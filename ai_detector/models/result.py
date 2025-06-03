"""Data models for detection results and analysis reports."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class DetectionLevel(Enum):
    """Confidence levels for AI detection."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class Language(Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    CSHARP = "csharp"
    UNKNOWN = "unknown"


@dataclass
class CodeFeatures:
    """Extracted features from code analysis."""
    # Structure metrics
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    function_count: int = 0
    class_count: int = 0
    
    # Comment analysis
    comment_ratio: float = 0.0
    docstring_ratio: float = 0.0
    comment_patterns: List[str] = field(default_factory=list)
    
    # Naming patterns
    variable_naming_score: float = 0.0
    function_naming_score: float = 0.0
    ai_typical_names: List[str] = field(default_factory=list)
    
    # Code style
    code_style_score: float = 0.0
    formatting_consistency: float = 0.0
    
    # Statistical features
    avg_line_length: float = 0.0
    blank_line_ratio: float = 0.0
    indentation_consistency: float = 0.0
    
    # AI-specific patterns
    ai_comment_patterns: int = 0
    ai_structure_patterns: int = 0
    ai_naming_patterns: int = 0
    
    # Language-specific features
    language_specific: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DetectionResult:
    """Result of AI code detection analysis."""
    # Core results
    is_ai_generated: bool
    confidence_score: float  # 0.0 to 1.0
    detection_level: DetectionLevel
    
    # Analysis details
    features: CodeFeatures
    language: Language
    file_path: Optional[str] = None
    
    # Reasoning
    reasons: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    analysis_time_ms: float = 0.0
    detector_version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "is_ai_generated": self.is_ai_generated,
            "confidence_score": self.confidence_score,
            "detection_level": self.detection_level.value,
            "language": self.language.value,
            "file_path": self.file_path,
            "reasons": self.reasons,
            "evidence": self.evidence,
            "features": {
                "lines_of_code": self.features.lines_of_code,
                "cyclomatic_complexity": self.features.cyclomatic_complexity,
                "comment_ratio": self.features.comment_ratio,
                "ai_patterns_detected": (
                    self.features.ai_comment_patterns +
                    self.features.ai_structure_patterns +
                    self.features.ai_naming_patterns
                )
            },
            "timestamp": self.timestamp.isoformat(),
            "analysis_time_ms": self.analysis_time_ms,
            "detector_version": self.detector_version
        }


@dataclass
class AnalysisReport:
    """Comprehensive analysis report for multiple files or entire repositories."""
    # Summary
    total_files: int = 0
    ai_generated_files: int = 0
    human_generated_files: int = 0
    uncertain_files: int = 0
    
    # Overall statistics
    average_confidence: float = 0.0
    languages_detected: List[Language] = field(default_factory=list)
    
    # Individual results
    file_results: List[DetectionResult] = field(default_factory=list)
    
    # Aggregated insights
    most_common_ai_patterns: List[str] = field(default_factory=list)
    risk_assessment: str = ""
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    analysis_start: datetime = field(default_factory=datetime.now)
    analysis_end: Optional[datetime] = None
    total_analysis_time_ms: float = 0.0
    
    @property
    def ai_percentage(self) -> float:
        """Percentage of files detected as AI-generated."""
        if self.total_files == 0:
            return 0.0
        return (self.ai_generated_files / self.total_files) * 100
    
    @property
    def human_percentage(self) -> float:
        """Percentage of files detected as human-generated."""
        if self.total_files == 0:
            return 0.0
        return (self.human_generated_files / self.total_files) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "summary": {
                "total_files": self.total_files,
                "ai_generated_files": self.ai_generated_files,
                "human_generated_files": self.human_generated_files,
                "uncertain_files": self.uncertain_files,
                "ai_percentage": self.ai_percentage,
                "human_percentage": self.human_percentage
            },
            "statistics": {
                "average_confidence": self.average_confidence,
                "languages_detected": [lang.value for lang in self.languages_detected],
                "total_analysis_time_ms": self.total_analysis_time_ms
            },
            "insights": {
                "most_common_ai_patterns": self.most_common_ai_patterns,
                "risk_assessment": self.risk_assessment,
                "recommendations": self.recommendations
            },
            "file_results": [result.to_dict() for result in self.file_results],
            "metadata": {
                "analysis_start": self.analysis_start.isoformat(),
                "analysis_end": self.analysis_end.isoformat() if self.analysis_end else None,
                "detector_version": "1.0.0"
            }
        } 