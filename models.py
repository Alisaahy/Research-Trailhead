"""
Database Models for Research Discovery Agent
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, Numeric, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model - stores researcher profiles"""
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Input data
    description = Column(Text)  # Manual description from user
    google_scholar_url = Column(String(500))
    google_scholar_data = Column(JSON)  # Scraped/imported data

    # AI-generated structured profile
    profile = Column(JSON)  # {
    #   "expertise_level": "PhD Student" | "Postdoc" | "Professor" | "Industry",
    #   "research_areas": ["NLP", "Computer Vision"],
    #   "specific_topics": ["Transformers", "Few-shot Learning"],
    #   "technical_skills": ["PyTorch", "HuggingFace"],
    #   "publication_count": 5,
    #   "h_index": 3,
    #   "research_style": "Empirical" | "Theoretical" | "Applied",
    #   "resource_access": "Limited" | "Moderate" | "Extensive",
    #   "novelty_preference": 0.7,  // 0-1
    #   "doability_preference": 0.8  // 0-1
    # }

    # Relationships
    papers = relationship("Paper", back_populates="user")

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'description': self.description,
            'google_scholar_url': self.google_scholar_url,
            'profile': self.profile
        }


class Paper(Base):
    """Paper model - stores uploaded research papers"""
    __tablename__ = 'papers'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(500))
    authors = Column(JSON)  # List of author names
    year = Column(Integer)
    venue = Column(String(200))
    doi = Column(String(100))
    pdf_filename = Column(String(255), nullable=False)
    pdf_size_bytes = Column(Integer)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=True)

    # Relationships
    user = relationship("User", back_populates="papers")
    analyses = relationship("Analysis", back_populates="paper", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'venue': self.venue,
            'doi': self.doi,
            'pdf_filename': self.pdf_filename,
            'pdf_size_bytes': self.pdf_size_bytes,
            'upload_timestamp': self.upload_timestamp.isoformat() if self.upload_timestamp else None,
            'user_id': self.user_id
        }


class Analysis(Base):
    """Analysis model - stores paper analysis jobs and results"""
    __tablename__ = 'analyses'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    paper_id = Column(String(36), ForeignKey('papers.id'), nullable=False)
    selected_topics = Column(JSON)  # List of topic strings
    user_profile_snapshot = Column(JSON)  # Snapshot of user profile at analysis time
    reader_output = Column(JSON)  # {summary, concepts, findings, limitations, ideas}
    searcher_output = Column(JSON)  # Intermediate searcher results
    status = Column(String(20), default='pending')  # pending, parsing, reading, ideas_ready, searching, complete, error
    progress = Column(Integer, default=0)  # 0-100
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    # Relationships
    paper = relationship("Paper", back_populates="analyses")
    ideas = relationship("ResearchIdea", back_populates="analysis", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'selected_topics': self.selected_topics,
            'reader_output': self.reader_output,
            'searcher_output': self.searcher_output,
            'status': self.status,
            'progress': self.progress,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class ResearchIdea(Base):
    """ResearchIdea model - stores ranked research ideas generated from analysis"""
    __tablename__ = 'research_ideas'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String(36), ForeignKey('analyses.id'), nullable=False)
    rank = Column(Integer)  # 1, 2, 3
    title = Column(String(500))
    description = Column(Text)
    rationale = Column(Text)

    # Scores
    novelty_score = Column(Numeric(3, 1))  # 1.0 - 5.0
    doability_score = Column(Numeric(3, 1))
    topic_match_score = Column(Numeric(3, 1))
    composite_score = Column(Numeric(3, 1))

    # Assessments (JSON objects)
    novelty_assessment = Column(JSON)  # {explored, maturity, gap, ...}
    doability_assessment = Column(JSON)  # {data_availability, methodology, ...}
    literature_synthesis = Column(JSON)  # {overview, whats_missing, suggested_approach, ...}

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    analysis = relationship("Analysis", back_populates="ideas")
    references = relationship("Reference", back_populates="idea", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'analysis_id': self.analysis_id,
            'rank': self.rank,
            'title': self.title,
            'description': self.description,
            'rationale': self.rationale,
            'novelty_score': float(self.novelty_score) if self.novelty_score else None,
            'doability_score': float(self.doability_score) if self.doability_score else None,
            'topic_match_score': float(self.topic_match_score) if self.topic_match_score else None,
            'composite_score': float(self.composite_score) if self.composite_score else None,
            'novelty_assessment': self.novelty_assessment,
            'doability_assessment': self.doability_assessment,
            'literature_synthesis': self.literature_synthesis,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Reference(Base):
    """Reference model - stores literature references for each research idea"""
    __tablename__ = 'references'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    idea_id = Column(String(36), ForeignKey('research_ideas.id'), nullable=False)
    title = Column(String(500))
    authors = Column(JSON)  # List of author names
    year = Column(Integer)
    venue = Column(String(200))
    abstract = Column(Text)
    url = Column(String(500))
    citation_count = Column(Integer)
    relevance_category = Column(String(50))  # 'foundational', 'recent', 'gap'
    summary = Column(Text)  # 2-3 sentence summary
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    idea = relationship("ResearchIdea", back_populates="references")

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'idea_id': self.idea_id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'venue': self.venue,
            'abstract': self.abstract,
            'url': self.url,
            'citation_count': self.citation_count,
            'relevance_category': self.relevance_category,
            'summary': self.summary,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
