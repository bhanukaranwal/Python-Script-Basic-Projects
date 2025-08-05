# Intelligent Personal Knowledge Graph Builder — main.py

import os
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from docx import Document
from PyPDF2 import PdfReader

# Load spaCy English model for named entity recognition (NER)
nlp = spacy.load("en_core_web_sm")

def extract_entities_relations(text):
    """
    Extract named entities and simplistic co-occurrence relationships from text.
    Returns list of entities and adds edges to a global graph G.
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Add nodes and co-occurrence edges between entities in this text block
    for ent, label in entities:
        if not G.has_node(ent):
            G.add_node(ent, label=label)

    # Add edges for pairs of entities co-occurring in the same text
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            ent1 = entities[i][0]
            ent2 = entities[j][0]
            if G.has_edge(ent1, ent2):
                G[ent1][ent2]['weight'] += 1
            else:
                G.add_edge(ent1, ent2, weight=1)
    return entities

def load_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def load_docx_file(filepath):
    doc = Document(filepath)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def load_pdf_file(filepath):
    reader = PdfReader(filepath)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_documents(folder_path):
    """
    Walk through folder_path, reading all documents (txt, docx, pdf).
    Extract entities and build the graph.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            text = ''
            try:
                if file.endswith('.txt'):
                    text = load_txt_file(full_path)
                elif file.endswith('.docx'):
                    text = load_docx_file(full_path)
                elif file.endswith('.pdf'):
                    text = load_pdf_file(full_path)
                else:
                    print(f"Unsupported file type: {file}")
                    continue
                print(f"Processing: {file}")
                extract_entities_relations(text)
            except Exception as e:
                print(f"Failed to process {file}: {e}")

def visualize_graph(graph):
    """
    Visualize the knowledge graph with matplotlib.
    Nodes sized by degree, colored by entity type.
    """
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(graph, k=0.5, iterations=50)

    labels = nx.get_node_attributes(graph, 'label')
    node_colors = []
    node_sizes = []
    color_map = {
        'PERSON': 'skyblue',
        'ORG': 'lightgreen',
        'GPE': 'orange',
        'DATE': 'pink',
        'LOC': 'yellow',
    }

    for node in graph.nodes():
        entity_type = labels.get(node, 'OTHER')
        node_colors.append(color_map.get(entity_type, 'lightgray'))
        node_sizes.append(300 + 50 * graph.degree(node))

    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.7)
    nx.draw_networkx_labels(graph, pos, font_size=8)

    plt.title('Personal Knowledge Graph')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    # Initialize global graph
    G = nx.Graph()

    # Folder containing your documents
    # Change this path to the folder with your personal documents
    documents_folder = 'documents/'

    print("Starting document processing and knowledge graph building...")
    process_documents(documents_folder)

    if len(G) == 0:
        print("No entities extracted. Please add documents in the 'documents/' folder.")
    else:
        print(f"Graph constructed with {len(G.nodes)} entities and {len(G.edges)} relationships.")
        visualize_graph(G)
