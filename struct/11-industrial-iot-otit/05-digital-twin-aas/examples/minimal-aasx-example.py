#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小 AASX 包生成示例
对齐：AAS Part 1 v3.2、AASX Package Format v3.0 (IDTA-01005)

生成一个包含 Digital Nameplate 和 Technical Data 两个 Submodel 的 AASX 文件，
可直接在 Eclipse AASX Package Explorer 或 BaSyx 中打开。
"""

import json
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def create_aas_json() -> dict:
    """创建符合 AAS Part 1 v3.2 的 JSON 序列化 AAS。"""
    return {
        "assetAdministrationShells": [
            {
                "id": "https://example.com/shells/Motor001",
                "idShort": "Motor001",
                "assetInformation": {
                    "assetKind": "Instance",
                    "globalAssetId": "https://example.com/assets/Motor001"
                },
                "submodels": [
                    {
                        "type": "ModelReference",
                        "keys": [
                            {
                                "type": "Submodel",
                                "value": "https://example.com/submodels/DigitalNameplate001"
                            }
                        ]
                    },
                    {
                        "type": "ModelReference",
                        "keys": [
                            {
                                "type": "Submodel",
                                "value": "https://example.com/submodels/TechnicalData001"
                            }
                        ]
                    }
                ],
                "modelType": "AssetAdministrationShell"
            }
        ],
        "submodels": [
            {
                "id": "https://example.com/submodels/DigitalNameplate001",
                "idShort": "DigitalNameplate",
                "semanticId": {
                    "type": "ExternalReference",
                    "keys": [
                        {
                            "type": "GlobalReference",
                            "value": "https://admin-shell.io/zvei/nameplate/2/0/Nameplate"
                        }
                    ]
                },
                "submodelElements": [
                    {
                        "idShort": "ManufacturerName",
                        "modelType": "Property",
                        "semanticId": {
                            "type": "ExternalReference",
                            "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAO677#002"}]
                        },
                        "valueType": "xs:string",
                        "value": "Example Motors GmbH"
                    },
                    {
                        "idShort": "ManufacturerProductDesignation",
                        "modelType": "Property",
                        "semanticId": {
                            "type": "ExternalReference",
                            "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAW338#001"}]
                        },
                        "valueType": "xs:string",
                        "value": "High Efficiency Motor HE-200"
                    },
                    {
                        "idShort": "SerialNumber",
                        "modelType": "Property",
                        "semanticId": {
                            "type": "ExternalReference",
                            "keys": [{"type": "GlobalReference", "value": "0173-1#02-AAM556#002"}]
                        },
                        "valueType": "xs:string",
                        "value": "SN-2026-001234"
                    }
                ],
                "modelType": "Submodel"
            },
            {
                "id": "https://example.com/submodels/TechnicalData001",
                "idShort": "TechnicalData",
                "semanticId": {
                    "type": "ExternalReference",
                    "keys": [
                        {
                            "type": "GlobalReference",
                            "value": "https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2"
                        }
                    ]
                },
                "submodelElements": [
                    {
                        "idShort": "Power",
                        "modelType": "Property",
                        "valueType": "xs:double",
                        "value": "15.0",
                        "unit": "kW"
                    },
                    {
                        "idShort": "Voltage",
                        "modelType": "Property",
                        "valueType": "xs:double",
                        "value": "400",
                        "unit": "V"
                    },
                    {
                        "idShort": "Frequency",
                        "modelType": "Property",
                        "valueType": "xs:double",
                        "value": "50",
                        "unit": "Hz"
                    }
                ],
                "modelType": "Submodel"
            }
        ],
        "conceptDescriptions": []
    }


def create_aasx_content_types() -> bytes:
    """生成 [Content_Types].xml（OOXML 包要求）。"""
    root = ET.Element("Types", xmlns="http://schemas.openxmlformats.org/package/2006/content-types")
    ET.SubElement(root, "Default", Extension="json", ContentType="text/plain")
    ET.SubElement(root, "Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(root, "Default", Extension="aas", ContentType="application/aas+xml")
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def create_rels() -> bytes:
    """生成 _rels/.rels（包关系）。"""
    root = ET.Element("Relationships", xmlns="http://schemas.openxmlformats.org/package/2006/relationships")
    ET.SubElement(
        root, "Relationship",
        Id="rId1",
        Type="http://admin-shell.io/aasx/relationships/aasx-origin",
        Target="aasx/aasx-origin.json"
    )
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def create_aasx_origin() -> bytes:
    """生成 aasx/aasx-origin.json（包标识）。"""
    return json.dumps({"aasxOrigin": "AASX Package v3.0"}, indent=2, ensure_ascii=False).encode("utf-8")


def create_aasx_rels() -> bytes:
    """生成 aasx/_rels/aasx-origin.json.rels（AAS 文件关系）。"""
    root = ET.Element("Relationships", xmlns="http://schemas.openxmlformats.org/package/2006/relationships")
    ET.SubElement(
        root, "Relationship",
        Id="rId1",
        Type="http://admin-shell.io/aasx/relationships/aas-spec",
        Target="../aasenv/Nameplate.aas.json"
    )
    return ET.tostring(root, encoding="UTF-8", xml_declaration=True)


def build_aasx(output_path: Path) -> None:
    """构建最小 AASX 包。"""
    aas_data = create_aas_json()

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # OOXML 包结构
        zf.writestr("[Content_Types].xml", create_aasx_content_types())
        zf.writestr("_rels/.rels", create_rels())
        zf.writestr("aasx/aasx-origin.json", create_aasx_origin())
        zf.writestr("aasx/_rels/aasx-origin.json.rels", create_aasx_rels())
        # AAS JSON 环境文件
        zf.writestr("aasenv/Nameplate.aas.json", json.dumps(aas_data, indent=2, ensure_ascii=False).encode("utf-8"))

    print(f"AASX 包已生成: {output_path}")
    print(f"  - AssetAdministrationShell: Motor001")
    print(f"  - Submodel: DigitalNameplate (Manufacturer, ProductDesignation, SerialNumber)")
    print(f"  - Submodel: TechnicalData (Power, Voltage, Frequency)")
    print(f"\n可用 Eclipse AASX Package Explorer 或 BaSyx 打开验证。")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="生成最小 AASX 示例包")
    parser.add_argument("--output", type=Path, default=Path("./minimal-example.aasx"), help="输出 AASX 文件路径")
    args = parser.parse_args()
    build_aasx(args.output)


if __name__ == "__main__":
    main()
