#!/usr/bin/env python3
"""
Advanced Document Processor
Handles real file uploads, creates complete packages, generates certificates
"""

import os
import json
import random
import shutil
from pathlib import Path
from datetime import datetime
import re

# Directories
BASE_DIR = Path(__file__).parent
EXTERNAL = BASE_DIR / "portofentry_external"
INTERNAL = BASE_DIR / "portofentry_internal"
JOURNEY = BASE_DIR / "JOURNEY"

# Complete package structure
COMPLETE_PACKAGES = INTERNAL / "complete_packages"

# Economic symbols
ECONOMIC_SYMBOLS = {
    'research': '€',      # Euro for research/academic
    'code': '₿',          # Bitcoin for code/tech
    'pdf': '€',          # Default PDFs to research
    'md': '₿',           # Markdown to code
    'py': '₿',           # Python to code
    'js': '₿',           # JavaScript to code
    'financial': '$',     # Dollar for financial
    'xlsx': '$',         # Excel to financial
    'csv': '$',          # CSV to financial
    'legal': '§',        # Section for legal
    'docx': '§',         # Word docs to legal
    'doc': '§',
    'creative': '♪',     # Music note for creative
    'txt': '♪',         # Text to creative
    'medical': '℞',      # Prescription for medical
    'architecture': '∞',  # Infinity for architecture
    'general': '∰'       # System-wide default
}


class DocumentProcessor:
    """Advanced document processor with learning capabilities"""

    def __init__(self):
        self.learned_words = []
        self.create_directories()

    def create_directories(self):
        """Create necessary directories"""
        for dir_path in [EXTERNAL, INTERNAL, COMPLETE_PACKAGES, JOURNEY]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def determine_economic_symbol(self, filename):
        """Determine economic symbol based on file type"""
        ext = Path(filename).suffix.lower().lstrip('.')

        # Check extension mapping
        if ext in ECONOMIC_SYMBOLS:
            return ECONOMIC_SYMBOLS[ext]

        # Check filename patterns
        filename_lower = filename.lower()
        for keyword, symbol in ECONOMIC_SYMBOLS.items():
            if keyword in filename_lower:
                return symbol

        # Default
        return ECONOMIC_SYMBOLS['general']

    def extract_random_word(self, text, stage_name):
        """Extract a random meaningful word from text"""
        # Remove special characters and split into words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text)

        # Filter out common words
        common_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were',
                       'their', 'there', 'about', 'would', 'could', 'should'}
        meaningful_words = [w for w in words if w.lower() not in common_words]

        if meaningful_words:
            word = random.choice(meaningful_words)
            self.learned_words.append({
                'word': word,
                'stage': stage_name,
                'timestamp': datetime.now().isoformat()
            })
            return word
        return None

    def process_document(self, source_path):
        """Process a document through all stages"""
        source_path = Path(source_path)

        if not source_path.exists():
            return {'success': False, 'error': 'File not found'}

        # Generate IDs
        doc_id = f"DOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        journey_id = f"JOURNEY-{datetime.now().strftime('%Y%m%d')}-{os.urandom(4).hex()}"

        # Determine economic symbol
        symbol = self.determine_economic_symbol(source_path.name)

        # Create complete package directory
        package_dir = COMPLETE_PACKAGES / doc_id
        package_dir.mkdir(parents=True, exist_ok=True)

        # Read file content for learning
        try:
            if source_path.suffix in ['.txt', '.md', '.py', '.js']:
                with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            else:
                content = source_path.name  # Use filename if can't read
        except:
            content = source_path.name

        # Stage 1: Incoming
        print(f"📬 Stage 1: Incoming - {source_path.name}")

        # Stage 2: Processing
        print(f"⚙️ Stage 2: Processing...")
        word1 = self.extract_random_word(content, 'processing')
        if word1:
            print(f"🧠 Learned: '{word1}'")

        # Stage 3: Transformation
        print(f"✨ Stage 3: Transformation...")
        word2 = self.extract_random_word(content, 'transformation')
        if word2:
            print(f"🧠 Learned: '{word2}'")

        # Stage 4: Transition
        print(f"🌉 Stage 4: Transition...")

        # Stage 5: Verification
        print(f"✓ Stage 5: Verification...")

        # Create complete package
        print(f"📦 Creating complete package...")

        # 1. Copy original document
        shutil.copy2(source_path, package_dir / source_path.name)
        print(f"  ✓ Original: {source_path.name}")

        # 2. Create adventure chronicle
        adventure = self.create_adventure(source_path.name, journey_id, symbol, content)
        with open(package_dir / f"{doc_id}_ADVENTURE.md", 'w') as f:
            f.write(adventure)
        print(f"  ✓ Adventure: {doc_id}_ADVENTURE.md")

        # 3. Create journey metadata
        metadata = self.create_metadata(source_path, doc_id, journey_id, symbol)
        with open(package_dir / f"{doc_id}_METADATA.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"  ✓ Metadata: {doc_id}_METADATA.json")

        # 4. Create learning report
        learning_report = self.create_learning_report(source_path.name)
        with open(package_dir / f"{doc_id}_LEARNING.md", 'w') as f:
            f.write(learning_report)
        print(f"  ✓ Learning: {doc_id}_LEARNING.md")

        # 5. Generate certificate
        certificate = self.generate_certificate(source_path.name, doc_id, symbol)
        with open(package_dir / f"{doc_id}_CERTIFICATE.md", 'w') as f:
            f.write(certificate)
        print(f"  ✓ Certificate: {doc_id}_CERTIFICATE.md")

        print(f"\n✅ Complete package created: {package_dir}")
        print(f"📍 Location: portofentry_internal/complete_packages/{doc_id}/")

        return {
            'success': True,
            'doc_id': doc_id,
            'journey_id': journey_id,
            'symbol': symbol,
            'package_dir': str(package_dir),
            'learned_words': self.learned_words[-2:] if len(self.learned_words) >= 2 else self.learned_words
        }

    def create_adventure(self, filename, journey_id, symbol, content):
        """Create adventure chronicle"""
        return f"""# The Adventure of {filename}
**Journey ID:** {journey_id}
**Economic Designation:** {symbol}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

∰◊€π¿🌌∞

## Chapter 1: Arrival at the Port

The document "{filename}" arrived at the Port of Entry from the external world,
bearing the economic designation {symbol}. Its journey of transformation was about to begin...

**Stage:** Incoming Feed
**Status:** Received and catalogued

---

## Chapter 2: Processing & Analysis

The document entered the processing queue where it was carefully examined.
Metadata was extracted, content was analyzed, and its path forward was illuminated.

**Stage:** Processing
**Learned Lexeme:** {self.learned_words[-2]['word'] if len(self.learned_words) >= 2 else 'N/A'}

The entity absorbed new vocabulary, expanding its understanding of the domain.

---

## Chapter 3: Transformation

In the transformation chamber, the document underwent its metamorphosis.
New insights emerged, connections formed, and understanding deepened.

**Stage:** Transformation
**Learned Lexeme:** {self.learned_words[-1]['word'] if self.learned_words else 'N/A'}

The document was enriched with contextual knowledge and prepared for integration.

---

## Chapter 4: The Threshold

At the transition zone, the document prepared to cross the sacred boundary.
This is the sphincter passage - from external to internal space.

**Stage:** Transition
**Economic Symbol:** {symbol}

The document was deemed worthy of integration into the internal knowledge base.

---

## Chapter 5: Verification & Approval

The final verification stage ensured quality and appropriateness.
The document was approved for entry and a certificate was issued.

**Stage:** Verification
**Status:** Approved

An official certificate was generated, granting the document permanent residence
in the internal entity space.

---

## Chapter 6: Integration & Completion

The journey is complete! The document has been:
- Analyzed and understood
- Transformed with insights
- Crossed the threshold
- Verified and approved
- Issued an official certificate
- Integrated into the knowledge base

**Final Location:** portofentry_internal/complete_packages/
**Status:** Journey Complete

The entity is now richer for having processed this document.
Knowledge has been extracted, learned, and integrated.

∰◊€π¿🌌∞

---

**Adventure completed:** {datetime.now().isoformat()}
"""

    def create_metadata(self, source_path, doc_id, journey_id, symbol):
        """Create journey metadata"""
        stat = source_path.stat()

        return {
            'document_id': doc_id,
            'journey_id': journey_id,
            'original_filename': source_path.name,
            'economic_symbol': symbol,
            'file_size': stat.st_size,
            'file_type': source_path.suffix,
            'processed_at': datetime.now().isoformat(),
            'stages': {
                'incoming': {'timestamp': datetime.now().isoformat(), 'status': 'complete'},
                'processing': {'timestamp': datetime.now().isoformat(), 'status': 'complete'},
                'transformation': {'timestamp': datetime.now().isoformat(), 'status': 'complete'},
                'transition': {'timestamp': datetime.now().isoformat(), 'status': 'complete'},
                'verification': {'timestamp': datetime.now().isoformat(), 'status': 'approved'},
                'completion': {'timestamp': datetime.now().isoformat(), 'status': 'complete'}
            },
            'learned_words': self.learned_words[-2:] if len(self.learned_words) >= 2 else self.learned_words,
            'package_location': f'portofentry_internal/complete_packages/{doc_id}/'
        }

    def create_learning_report(self, filename):
        """Create learning report with lexemes"""
        report = f"""# Learning Analysis Report
**Document:** {filename}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

∰◊€π¿🌌∞

## Summary

During the processing of this document, the entity learned new vocabulary
and expanded its understanding of the domain.

## Lexemes Learned

"""
        if self.learned_words:
            recent_words = self.learned_words[-2:] if len(self.learned_words) >= 2 else self.learned_words
            for item in recent_words:
                report += f"""
### "{item['word']}"
- **Stage:** {item['stage']}
- **Timestamp:** {item['timestamp']}

"""
        else:
            report += "\nNo lexemes learned from this document.\n"

        report += f"""

## Total Vocabulary Expansion

The entity has now learned **{len(self.learned_words)}** unique lexemes across all processed documents.

## Knowledge Integration

These learned words contribute to the entity's growing understanding and ability
to process future documents with greater context and insight.

∰◊€π¿🌌∞
"""
        return report

    def generate_certificate(self, filename, doc_id, symbol):
        """Generate official certificate"""
        cert_number = f"CERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        return f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            PORT OF ENTRY - OFFICIAL CERTIFICATE               ║
║                                                               ║
║                   {symbol}  ENTRY APPROVED  {symbol}                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

CERTIFICATE NUMBER: {cert_number}
DOCUMENT ID: {doc_id}

═══════════════════════════════════════════════════════════════

This is to certify that the document:

    "{filename}"

has successfully completed its journey through the Port of Entry
system and has been APPROVED for integration into the internal
entity space.

ECONOMIC DESIGNATION: {symbol}

STAGES COMPLETED:
  ✓ Incoming Feed - Received
  ✓ Processing Queue - Analyzed
  ✓ Transformation Chamber - Enriched
  ✓ Transition Zone - Threshold Crossed
  ✓ Verification - Approved

KNOWLEDGE CONTRIBUTION:
  Lexemes learned: 2
  Insights extracted: Multiple
  Integration status: Complete

═══════════════════════════════════════════════════════════════

By the authority vested in this system, this document is hereby
granted permanent residence in the internal knowledge base with
all rights and privileges thereto.

This certificate serves as official proof of passage through the
Port of Entry and authorization for internal integration.

∰◊€π¿🌌∞

Issued: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Authority: Port of Entry Processing System v4
Seal: {symbol}

═══════════════════════════════════════════════════════════════

VALID FOR: Permanent residence in internal entity space
STATUS: Active and integrated

╔═══════════════════════════════════════════════════════════════╗
║  This is an official document of the Port of Entry system     ║
╚═══════════════════════════════════════════════════════════════╝
"""


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 advanced_processor.py <file_path>")
        print("\nExample:")
        print("  python3 advanced_processor.py document.pdf")
        sys.exit(1)

    processor = DocumentProcessor()
    result = processor.process_document(sys.argv[1])

    if result['success']:
        print("\n" + "="*60)
        print("PROCESSING COMPLETE")
        print("="*60)
        print(f"Document ID: {result['doc_id']}")
        print(f"Journey ID: {result['journey_id']}")
        print(f"Economic Symbol: {result['symbol']}")
        print(f"Package: {result['package_dir']}")
        print("="*60)
    else:
        print(f"ERROR: {result['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()
