"""Generates docs/architecture-bedrock.drawio for the Bedrock/LLM chatbot variant using drawpyo.

Run with: python3 scripts/generate_diagram_bedrock.py
"""
import os

import drawpyo

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

AWS4_BASE = (
    "sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;strokeColor=none;"
    "dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;"
    "fontSize=11;fontStyle=0;aspect=fixed;pointerEvents=1;"
)


def aws_style(icon_name, fill_color):
    return f"{AWS4_BASE}fillColor={fill_color};shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon_name};"


def add_node(page, name, x, y, icon_name, fill_color, width=64, height=64):
    node = drawpyo.diagram.Object(page=page, value=name)
    node.position = (x, y)
    node.geometry.width = width
    node.geometry.height = height
    node.apply_style_string(aws_style(icon_name, fill_color))
    return node


def add_group(page, name, x, y, width, height):
    group = drawpyo.diagram.Object(page=page, value=name)
    group.position = (x, y)
    group.geometry.width = width
    group.geometry.height = height
    group.apply_style_string(
        "rounded=0;whiteSpace=wrap;html=1;dashed=0;fillColor=none;"
        "strokeColor=#146EB4;verticalAlign=top;align=left;fontColor=#146EB4;fontSize=12;"
        "spacingLeft=6;spacingTop=4;"
    )
    return group


def add_edge(page, source, target, label=None, bidirectional=False):
    edge = drawpyo.diagram.Edge(page=page, source=source, target=target, label=label)
    edge.waypoints = "orthogonal"
    edge.endArrow = "block"
    edge.startArrow = "block" if bidirectional else "none"
    edge.strokeColor = "#545B64"
    return edge


def build_diagram():
    file = drawpyo.File()
    file.file_name = "architecture-bedrock.drawio"
    file.file_path = OUTPUT_DIR

    page = drawpyo.Page(file=file)
    page.name = "Chatbot Architecture (Bedrock)"

    aws_cloud = add_group(page, "AWS Cloud", 180, 40, 640, 460)

    end_users = add_node(page, "End users\n(web / mobile)", 40, 280, "client", "#232F3E")

    cognito = add_node(page, "Amazon Cognito\n(user authentication)", 220, 80, "cognito", "#DD344C")
    lambda_fn = add_node(page, "AWS Lambda\n(chat orchestrator)", 260, 280, "lambda_function", "#ED7100")
    bedrock = add_node(page, "Amazon Bedrock\n(foundation model / LLM)", 460, 280, "machine_learning", "#01A88D")
    dynamodb = add_node(page, "Amazon DynamoDB\n(conversation & data store)", 660, 280, "dynamodb", "#C925D1")

    add_edge(page, end_users, cognito, "Sign in", bidirectional=True)
    add_edge(page, end_users, lambda_fn, "Send message / Bot response", bidirectional=True)
    add_edge(page, lambda_fn, bedrock, "Invoke model", bidirectional=True)
    add_edge(page, lambda_fn, dynamodb, "Read / write history", bidirectional=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file.write()
    print(f"Wrote {os.path.join(OUTPUT_DIR, file.file_name)}")


if __name__ == "__main__":
    build_diagram()
