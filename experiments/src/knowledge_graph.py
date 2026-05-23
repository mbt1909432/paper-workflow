"""Simple knowledge graph construction from document contexts."""
import json
import re
from dataclasses import dataclass, field


@dataclass
class Entity:
    name: str
    description: str = ""


@dataclass
class Relation:
    head: str
    relation: str
    tail: str


@dataclass
class KnowledgeGraph:
    entities: dict[str, Entity] = field(default_factory=dict)
    relations: list[Relation] = field(default_factory=list)

    def add_entity(self, name: str, description: str = ""):
        if name not in self.entities:
            self.entities[name] = Entity(name=name, description=description)

    def add_relation(self, head: str, relation: str, tail: str):
        self.add_entity(head)
        self.add_entity(tail)
        self.relations.append(Relation(head=head, relation=relation, tail=tail))

    def get_neighbors(self, entity_name: str) -> list[Relation]:
        """Get all relations involving an entity."""
        return [
            r for r in self.relations
            if r.head == entity_name or r.tail == entity_name
        ]

    def get_subgraph(self, entities: list[str], max_hops: int = 2) -> list[Relation]:
        """Get subgraph around given entities within max_hops."""
        visited = set(entities)
        result = []
        frontier = set(entities)

        for _ in range(max_hops):
            next_frontier = set()
            for rel in self.relations:
                if rel.head in frontier or rel.tail in frontier:
                    if rel not in result:
                        result.append(rel)
                    if rel.head not in visited:
                        next_frontier.add(rel.head)
                    if rel.tail not in visited:
                        next_frontier.add(rel.tail)
            visited.update(next_frontier)
            frontier = next_frontier
            if not frontier:
                break

        return result

    def subgraph_to_text(self, relations: list[Relation]) -> str:
        """Convert subgraph relations to natural text."""
        lines = []
        for r in relations:
            lines.append(f"- {r.head} {r.relation} {r.tail}")
        return "\n".join(lines)

    def stats(self) -> str:
        return f"KG: {len(self.entities)} entities, {len(self.relations)} relations"


def build_kg_from_hotpotqa(example: dict) -> KnowledgeGraph:
    """Build a knowledge graph from a HotpotQA example's supporting facts."""
    kg = KnowledgeGraph()

    # Extract facts from supporting paragraphs
    supporting_titles = set()
    if "supporting_facts" in example:
        for title, sent_ids in example["supporting_facts"]:
            supporting_titles.add(title)

    # Build entities and relations from context paragraphs
    for title, sentences in example.get("context", []):
        kg.add_entity(title, description=" ".join(sentences[:2]))
        for other_title in supporting_titles:
            if other_title != title:
                # Co-occurrence relation (shared question context)
                kg.add_relation(title, "related_to", other_title)

    # Extract named entities from the question using simple heuristics
    question = example.get("question", "")
    answer = example.get("answer", "")

    # Add answer entity
    if answer and answer not in ("yes", "no"):
        kg.add_entity(answer)
        for title in supporting_titles:
            kg.add_relation(answer, "answer_from", title)

    return kg


def build_kg_from_documents(documents: list[str]) -> KnowledgeGraph:
    """Build a simple KG by extracting (subject, relation, object) patterns."""
    kg = KnowledgeGraph()

    for doc in documents:
        # Simple pattern: sentences with "is", "was", "are", "has"
        sentences = doc.split(". ")
        for sent in sentences:
            for pattern in [r"(.+?)\s+(?:is|was|are|were)\s+(.+?)(?:\.|$)",
                          r"(.+?)\s+has\s+(.+?)(?:\.|$)",
                          r"(.+?)\s+located\s+in\s+(.+?)(?:\.|$)"]:
                match = re.search(pattern, sent)
                if match:
                    subj = match.group(1).strip()
                    obj = match.group(2).strip()
                    if len(subj) < 50 and len(obj) < 50:
                        kg.add_entity(subj)
                        kg.add_entity(obj)
                        rel_type = "is" if "is" in pattern or "was" in pattern else "has" if "has" in pattern else "located_in"
                        kg.add_relation(subj, rel_type, obj)

    return kg
