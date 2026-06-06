-------------------------------- MODULE FXConnectionManager --------------------------------
(*
 * FX Connection Manager State Machine TLA+ Specification
 * 
 * Version: 2026-06-06
 * Standard: OPC UA FX Part 80-84, IEC 62541-100
 * 
 * This specification models the lifecycle of an OPC UA FX Connection Manager,
 * covering the states: Offline -> Discovery -> Configuration -> Operational
 * with transitions to Error and Teardown.
 *
 * Invariants:
 *   1. CapabilityMatch: Both endpoints must agree on supported features
 *      before entering Operational.
 *   2. HeartbeatTimeout: Missing heartbeats trigger failover to Error.
 *   3. DeterminismPreservation: Once Operational, scheduling parameters
 *      must remain stable unless a controlled reconfiguration occurs.
 *)

EXTENDS Integers, Sequences, FiniteSets

--------------------------------------------------------------------------------
-- Constants and Parameters
--------------------------------------------------------------------------------

CONSTANTS
    EndpointId,              (* Set of all endpoint identifiers {A, B} for a single connection *)
    FeatureSet,              (* Set of supported features: {"C2C", "C2D", "D2D", "TSN", "Safety"} *)
    MaxHeartbeatMiss,        (* Maximum allowed missed heartbeats before failover *)
    MaxRetryCount            (* Maximum retry attempts for Discovery/Configuration *)

ASSUME MaxHeartbeatMiss \in Nat /\ MaxHeartbeatMiss > 0
ASSUME MaxRetryCount \in Nat /\ MaxRetryCount > 0

--------------------------------------------------------------------------------
-- State Definitions
--------------------------------------------------------------------------------

(* ConnectionManagerState represents the global state of a single FX connection *)
CMStates == {"Offline", "Discovery", "Configuration", "Operational", "Error", "Teardown"}

(* Per-endpoint local states during capability negotiation *)
EndpointStates == {"Idle", "Announced", "Acked", "Rejected"}

--------------------------------------------------------------------------------
-- Variables
--------------------------------------------------------------------------------

VARIABLES
    cmState,                 (* Global Connection Manager state: CMStates *)
    endpointState,           (* endpointState[e] \in EndpointStates for each e \in EndpointId *)
    localFeatures,           (* localFeatures[e] \subseteq FeatureSet: features supported by endpoint e *)
    agreedFeatures,          (* agreedFeatures[e] \subseteq FeatureSet: features agreed upon *)
    heartbeatCounter,        (* heartbeatCounter[e]: consecutive missed heartbeats *)
    retryCounter,            (* retryCounter: number of failed Discovery/Config attempts *)
    configStable,            (* configStable \in BOOLEAN: true if scheduling params are locked *)
    networkAvailable         (* networkAvailable \in BOOLEAN: underlying TSN link status *)

--------------------------------------------------------------------------------
-- Type Invariants
--------------------------------------------------------------------------------

TypeInvariant ==
    /\ cmState \in CMStates
    /\ endpointState \in [EndpointId -> EndpointStates]
    /\ localFeatures \in [EndpointId -> SUBSET FeatureSet]
    /\ agreedFeatures \in [EndpointId -> SUBSET FeatureSet]
    /\ heartbeatCounter \in [EndpointId -> Nat]
    /\ retryCounter \in Nat
    /\ configStable \in BOOLEAN
    /\ networkAvailable \in BOOLEAN

--------------------------------------------------------------------------------
-- Helper Operators
--------------------------------------------------------------------------------

(* All endpoints have reached a given state *)
AllEndpointsIn(st) == \A e \in EndpointId : endpointState[e] = st

(* Capability match: both endpoints agree on a non-empty intersection of features *)
CapabilitiesMatch ==
    /\ AllEndpointsIn("Acked")
    /\ \A e \in EndpointId : agreedFeatures[e] # {}
    /\ \E common \in SUBSET FeatureSet :
        /\ common # {}
        /\ \A e \in EndpointId : common \subseteq agreedFeatures[e]

(* At least one endpoint has rejected *)
AnyEndpointRejected == \E e \in EndpointId : endpointState[e] = "Rejected"

(* Heartbeat timeout condition for any endpoint *)
HeartbeatTimeout == \E e \in EndpointId : heartbeatCounter[e] >= MaxHeartbeatMiss

(* Reset all endpoint states *)
ResetEndpoints == [e \in EndpointId |-> "Idle"]

--------------------------------------------------------------------------------
-- Initial State
--------------------------------------------------------------------------------

Init ==
    /\ cmState = "Offline"
    /\ endpointState = [e \in EndpointId |-> "Idle"]
    /\ localFeatures \in [EndpointId -> SUBSET FeatureSet]
    /\ agreedFeatures = [e \in EndpointId |-> {}]
    /\ heartbeatCounter = [e \in EndpointId |-> 0]
    /\ retryCounter = 0
    /\ configStable = FALSE
    /\ networkAvailable = TRUE

--------------------------------------------------------------------------------
-- Actions / Transitions
--------------------------------------------------------------------------------

(* OFFLINE -> DISCOVERY: Start discovery when network is available *)
StartDiscovery ==
    /\ cmState = "Offline"
    /\ networkAvailable = TRUE
    /\ cmState' = "Discovery"
    /\ endpointState' = [e \in EndpointId |-> "Announced"]
    /\ agreedFeatures' = [e \in EndpointId |-> {}]
    /\ retryCounter' = 0
    /\ UNCHANGED <<localFeatures, heartbeatCounter, configStable, networkAvailable>>

(* DISCOVERY: Endpoint acknowledges capabilities *)
AcknowledgeCapabilities(e) ==
    /\ cmState = "Discovery"
    /\ endpointState[e] = "Announced"
    /\ endpointState' = [endpointState EXCEPT ![e] = "Acked"]
    /\ agreedFeatures' = [agreedFeatures EXCEPT ![e] = localFeatures[e]]
    /\ UNCHANGED <<cmState, localFeatures, heartbeatCounter, retryCounter, configStable, networkAvailable>>

(* DISCOVERY -> CONFIGURATION: All endpoints acked and capabilities match *)
DiscoveryToConfiguration ==
    /\ cmState = "Discovery"
    /\ CapabilitiesMatch
    /\ cmState' = "Configuration"
    /\ configStable' = FALSE
    /\ UNCHANGED <<endpointState, localFeatures, agreedFeatures, heartbeatCounter, retryCounter, networkAvailable>>

(* DISCOVERY -> ERROR: Capability mismatch or max retries reached *)
DiscoveryFail ==
    /\ cmState = "Discovery"
    /\ (AnyEndpointRejected \/ retryCounter >= MaxRetryCount)
    /\ cmState' = "Error"
    /\ endpointState' = ResetEndpoints
    /\ UNCHANGED <<localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable, networkAvailable>>

(* DISCOVERY retry: Not all acked, increment retry *)
DiscoveryRetry ==
    /\ cmState = "Discovery"
    /\ ~CapabilitiesMatch
    /\ ~AnyEndpointRejected
    /\ retryCounter < MaxRetryCount
    /\ retryCounter' = retryCounter + 1
    /\ endpointState' = [e \in EndpointId |-> "Announced"]
    /\ UNCHANGED <<cmState, localFeatures, agreedFeatures, heartbeatCounter, configStable, networkAvailable>>

(* CONFIGURATION: Lock scheduling parameters *)
LockConfiguration ==
    /\ cmState = "Configuration"
    /\ configStable = FALSE
    /\ configStable' = TRUE
    /\ UNCHANGED <<cmState, endpointState, localFeatures, agreedFeatures, heartbeatCounter, retryCounter, networkAvailable>>

(* CONFIGURATION -> OPERATIONAL: Configuration stable and network ready *)
ConfigurationToOperational ==
    /\ cmState = "Configuration"
    /\ configStable = TRUE
    /\ networkAvailable = TRUE
    /\ cmState' = "Operational"
    /\ heartbeatCounter' = [e \in EndpointId |-> 0]
    /\ UNCHANGED <<endpointState, localFeatures, agreedFeatures, retryCounter, configStable, networkAvailable>>

(* CONFIGURATION -> ERROR: Configuration timeout or network lost *)
ConfigurationFail ==
    /\ cmState = "Configuration"
    /\ (~networkAvailable \/ retryCounter >= MaxRetryCount)
    /\ cmState' = "Error"
    /\ endpointState' = ResetEndpoints
    /\ UNCHANGED <<localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable, networkAvailable>>

(* OPERATIONAL: Send/Receive heartbeat *)
Heartbeat(e) ==
    /\ cmState = "Operational"
    /\ networkAvailable = TRUE
    /\ heartbeatCounter' = [heartbeatCounter EXCEPT ![e] = 0]
    /\ UNCHANGED <<cmState, endpointState, localFeatures, agreedFeatures, retryCounter, configStable, networkAvailable>>

(* OPERATIONAL: Missed heartbeat detection *)
MissedHeartbeat(e) ==
    /\ cmState = "Operational"
    /\ networkAvailable = TRUE
    /\ heartbeatCounter' = [heartbeatCounter EXCEPT ![e] = @ + 1]
    /\ UNCHANGED <<cmState, endpointState, localFeatures, agreedFeatures, retryCounter, configStable, networkAvailable>>

(* OPERATIONAL -> ERROR: Heartbeat timeout *)
OperationalFail ==
    /\ cmState = "Operational"
    /\ HeartbeatTimeout
    /\ cmState' = "Error"
    /\ endpointState' = ResetEndpoints
    /\ UNCHANGED <<localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable, networkAvailable>>

(* OPERATIONAL -> TEARDOWN: Graceful shutdown request *)
OperationalToTeardown ==
    /\ cmState = "Operational"
    /\ cmState' = "Teardown"
    /\ endpointState' = ResetEndpoints
    /\ UNCHANGED <<localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable, networkAvailable>>

(* ERROR -> OFFLINE: Reset and recover *)
ErrorToOffline ==
    /\ cmState = "Error"
    /\ cmState' = "Offline"
    /\ endpointState' = ResetEndpoints
    /\ agreedFeatures' = [e \in EndpointId |-> {}]
    /\ heartbeatCounter' = [e \in EndpointId |-> 0]
    /\ retryCounter' = 0
    /\ configStable' = FALSE
    /\ UNCHANGED <<localFeatures, networkAvailable>>

(* TEARDOWN -> OFFLINE: Cleanup complete *)
TeardownToOffline ==
    /\ cmState = "Teardown"
    /\ cmState' = "Offline"
    /\ endpointState' = ResetEndpoints
    /\ agreedFeatures' = [e \in EndpointId |-> {}]
    /\ heartbeatCounter' = [e \in EndpointId |-> 0]
    /\ retryCounter' = 0
    /\ configStable' = FALSE
    /\ UNCHANGED <<localFeatures, networkAvailable>>

(* Network failure: any state -> Error (except Offline/Teardown) *)
NetworkFailure ==
    /\ cmState \in {"Discovery", "Configuration", "Operational"}
    /\ networkAvailable = TRUE
    /\ networkAvailable' = FALSE
    /\ cmState' = "Error"
    /\ endpointState' = ResetEndpoints
    /\ UNCHANGED <<localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable>>

(* Network recovery *)
NetworkRecover ==
    /\ networkAvailable = FALSE
    /\ networkAvailable' = TRUE
    /\ UNCHANGED <<cmState, endpointState, localFeatures, agreedFeatures, heartbeatCounter, retryCounter, configStable>>

--------------------------------------------------------------------------------
-- Next State Relation
--------------------------------------------------------------------------------

Next ==
    \/ StartDiscovery
    \/ \E e \in EndpointId : AcknowledgeCapabilities(e)
    \/ DiscoveryToConfiguration
    \/ DiscoveryFail
    \/ DiscoveryRetry
    \/ LockConfiguration
    \/ ConfigurationToOperational
    \/ ConfigurationFail
    \/ \E e \in EndpointId : Heartbeat(e)
    \/ \E e \in EndpointId : MissedHeartbeat(e)
    \/ OperationalFail
    \/ OperationalToTeardown
    \/ ErrorToOffline
    \/ TeardownToOffline
    \/ NetworkFailure
    \/ NetworkRecover

--------------------------------------------------------------------------------
-- Specification
--------------------------------------------------------------------------------

Spec == Init /\ [][Next]_vars

vars == <<cmState, endpointState, localFeatures, agreedFeatures, 
           heartbeatCounter, retryCounter, configStable, networkAvailable>>

--------------------------------------------------------------------------------
-- Invariants (Safety Properties)
--------------------------------------------------------------------------------

(* INV-1: CapabilityMatchInvariant -- Operational implies capabilities matched *)
CapabilityMatchInvariant ==
    cmState = "Operational" => CapabilitiesMatch

(* INV-2: ConfigurationStableInvariant -- Operational implies config is stable *)
ConfigurationStableInvariant ==
    cmState = "Operational" => configStable = TRUE

(* INV-3: HeartbeatBoundedInvariant -- heartbeatCounter never exceeds MaxHeartbeatMiss in Operational *)
HeartbeatBoundedInvariant ==
    cmState = "Operational" => \A e \in EndpointId : heartbeatCounter[e] <= MaxHeartbeatMiss

(* INV-4: OfflineNoFeatures -- Offline/Teardown implies no agreed features *)
OfflineNoFeatures ==
    cmState \in {"Offline", "Teardown"} => \A e \in EndpointId : agreedFeatures[e] = {}

(* INV-5: ErrorImpliesReset -- Error state implies endpoints are Idle *)
ErrorImpliesReset ==
    cmState = "Error" => AllEndpointsIn("Idle")

--------------------------------------------------------------------------------
-- Liveness Properties
--------------------------------------------------------------------------------

(* LIVE-1: DiscoveryProgress -- If in Discovery with matching capabilities, eventually Configuration *)
DiscoveryProgress ==
    cmState = "Discovery" /\ CapabilitiesMatch ~> cmState = "Configuration"

(* LIVE-2: ConfigurationProgress -- If in Configuration with stable config and network, eventually Operational *)
ConfigurationProgress ==
    cmState = "Configuration" /\ configStable /\ networkAvailable ~> cmState = "Operational"

(* LIVE-3: ErrorRecovery -- Error state eventually leads to Offline (recoverable) *)
ErrorRecovery ==
    cmState = "Error" ~> cmState = "Offline"

--------------------------------------------------------------------------------
-- Theorems
--------------------------------------------------------------------------------

THEOREM Spec => [](TypeInvariant)
THEOREM Spec => []CapabilityMatchInvariant
THEOREM Spec => []ConfigurationStableInvariant
THEOREM Spec => []HeartbeatBoundedInvariant
THEOREM Spec => []OfflineNoFeatures
THEOREM Spec => []ErrorImpliesReset

================================================================================
