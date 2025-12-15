#!/usr/bin/env python3
"""
Port of Entry v0 - API Server
Connects the UI to real document processing
"""

import http.server
import socketserver
import json
import os
import sys
import threading
import time
from pathlib import Path
from datetime import datetime
import urllib.parse
import shutil

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from advanced_processor import DocumentProcessor

PORT = 8000
BASE_DIR = Path(__file__).parent.resolve()

# Directories
INCOMING = Path("/home/sauron/portofentry_external/incoming")
INTERNAL = BASE_DIR / "portofentry_internal"
COMPLETE_PACKAGES = INTERNAL / "complete_packages"

# Ensure directories exist
INCOMING.mkdir(parents=True, exist_ok=True)
COMPLETE_PACKAGES.mkdir(parents=True, exist_ok=True)

# Stats
stats = {
    'total_processed': 0,
    'session_processed': 0,
    'total_learned': 0,
    'server_started': datetime.now().isoformat()
}


class PortOfEntryServer(http.server.SimpleHTTPRequestHandler):
    """API server for Port of Entry v0"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)

        # API endpoints
        if parsed_path.path == '/api/documents':
            self.list_documents()
        elif parsed_path.path == '/api/stats':
            self.get_stats()
        elif parsed_path.path == '/api/complete':
            self.list_complete()
        elif parsed_path.path.startswith('/api/package/'):
            self.get_package_content(parsed_path.path)
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_path = urllib.parse.urlparse(self.path)

        if parsed_path.path == '/api/process':
            self.process_document(post_data)
        elif parsed_path.path == '/api/process_all':
            self.process_all(post_data)
        else:
            self.send_error(404, "API endpoint not found")

    def list_documents(self):
        """List documents in incoming directory"""
        try:
            documents = []

            if INCOMING.exists():
                for file_path in sorted(INCOMING.iterdir()):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        # Get file info
                        stat = file_path.stat()

                        # Determine economic symbol
                        processor = DocumentProcessor()
                        symbol = processor.determine_economic_symbol(file_path.name)

                        # Determine type
                        ext = file_path.suffix.lower().lstrip('.')
                        type_map = {
                            'pdf': 'research',
                            'md': 'code',
                            'py': 'code',
                            'js': 'code',
                            'xlsx': 'financial',
                            'csv': 'financial',
                            'docx': 'legal',
                            'doc': 'legal',
                            'txt': 'creative'
                        }
                        doc_type = type_map.get(ext, 'general')

                        documents.append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'size': self.format_size(stat.st_size),
                            'type': doc_type,
                            'symbol': symbol,
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })

            self.send_json_response({
                'success': True,
                'documents': documents,
                'count': len(documents)
            })

        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    def process_document(self, post_data):
        """Process a single document"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            doc_path = data.get('path')

            if not doc_path or not Path(doc_path).exists():
                raise ValueError("Invalid document path")

            # Process the document
            processor = DocumentProcessor()
            result = processor.process_document(doc_path)

            if result['success']:
                # Remove from incoming (move to processed)
                try:
                    Path(doc_path).unlink()
                except:
                    pass  # File might already be moved

                # Update stats
                stats['total_processed'] += 1
                stats['session_processed'] += 1
                stats['total_learned'] += len(result.get('learned_words', []))

                self.send_json_response({
                    'success': True,
                    'message': f"Document processed successfully",
                    'doc_id': result['doc_id'],
                    'journey_id': result['journey_id'],
                    'symbol': result['symbol'],
                    'package_dir': result['package_dir'],
                    'learned_words': result.get('learned_words', [])
                })
            else:
                self.send_json_response({
                    'success': False,
                    'error': result.get('error', 'Processing failed')
                }, status=500)

        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    def process_all(self, post_data):
        """Process all documents (batch of 5)"""
        try:
            data = json.loads(post_data.decode('utf-8'))
            documents = data.get('documents', [])
            batch_size = min(len(documents), 5)  # Process max 5 at a time

            results = []
            processor = DocumentProcessor()

            for i in range(batch_size):
                doc_path = documents[i]['path']

                if Path(doc_path).exists():
                    result = processor.process_document(doc_path)

                    if result['success']:
                        # Remove from incoming
                        try:
                            Path(doc_path).unlink()
                        except:
                            pass

                        # Update stats
                        stats['total_processed'] += 1
                        stats['session_processed'] += 1
                        stats['total_learned'] += len(result.get('learned_words', []))

                        results.append({
                            'name': documents[i]['name'],
                            'success': True,
                            'doc_id': result['doc_id']
                        })
                    else:
                        results.append({
                            'name': documents[i]['name'],
                            'success': False,
                            'error': result.get('error', 'Unknown error')
                        })

            self.send_json_response({
                'success': True,
                'processed': len(results),
                'results': results
            })

        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    def list_complete(self):
        """List completed packages"""
        try:
            packages = []

            if COMPLETE_PACKAGES.exists():
                for package_dir in sorted(COMPLETE_PACKAGES.iterdir(), reverse=True):
                    if package_dir.is_dir():
                        # Read metadata
                        metadata_files = list(package_dir.glob('*_METADATA.json'))
                        if metadata_files:
                            with open(metadata_files[0], 'r') as f:
                                metadata = json.load(f)

                            packages.append({
                                'doc_id': metadata.get('document_id'),
                                'filename': metadata.get('original_filename'),
                                'symbol': metadata.get('economic_symbol'),
                                'processed_at': metadata.get('processed_at'),
                                'learned_words': len(metadata.get('learned_words', []))
                            })

            self.send_json_response({
                'success': True,
                'packages': packages,
                'count': len(packages)
            })

        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=500)

    def get_stats(self):
        """Get server statistics"""
        self.send_json_response({
            'success': True,
            'stats': stats
        })

    def get_package_content(self, path):
        """Get content from a specific package"""
        try:
            # Parse path: /api/package/<doc_id>/<content_type>
            parts = path.split('/')
            if len(parts) < 5:
                raise ValueError("Invalid package path")

            doc_id = parts[3]
            content_type = parts[4]

            # Find package directory
            package_dir = COMPLETE_PACKAGES / doc_id
            if not package_dir.exists():
                raise ValueError("Package not found")

            # Determine which file to read
            file_map = {
                'metadata': f'{doc_id}_METADATA.json',
                'adventure': f'{doc_id}_ADVENTURE.md',
                'learning': f'{doc_id}_LEARNING.md',
                'certificate': f'{doc_id}_CERTIFICATE.md',
            }

            if content_type == 'original':
                # Find the original file (not one of the generated files)
                original_files = [f for f in package_dir.iterdir()
                                if f.is_file() and not any(f.name.endswith(suffix)
                                for suffix in ['_METADATA.json', '_ADVENTURE.md',
                                             '_LEARNING.md', '_CERTIFICATE.md'])]
                if original_files:
                    target_file = original_files[0]
                else:
                    raise ValueError("Original file not found")
            else:
                filename = file_map.get(content_type)
                if not filename:
                    raise ValueError("Invalid content type")
                target_file = package_dir / filename

            if not target_file.exists():
                raise ValueError(f"File not found: {target_file.name}")

            # Read and return content
            with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Determine response type
            file_type = 'json' if target_file.suffix == '.json' else 'markdown'

            self.send_json_response({
                'success': True,
                'content': json.loads(content) if file_type == 'json' else content,
                'type': file_type,
                'filename': target_file.name
            })

        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, status=404)

    def format_size(self, bytes):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        """Custom log format"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {format % args}")


def print_banner():
    """Print server banner"""
    print("=" * 70)
    print("∰◊€π¿🌌∞ PORT OF ENTRY v0 - API SERVER ∰◊€π¿🌌∞".center(70))
    print("=" * 70)
    print()
    print(f"🌐 Server URL:        http://localhost:{PORT}")
    print(f"📂 Incoming:          {INCOMING}")
    print(f"📦 Complete Packages: {COMPLETE_PACKAGES}")
    print()
    print("📺 Open UI: http://localhost:8000/document_processor_v4.html")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()


def main():
    """Start the server"""
    print_banner()

    with socketserver.TCPServer(("", PORT), PortOfEntryServer) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()
            print("\n" + "=" * 70)
            print(f"✅ Processed {stats['session_processed']} documents this session")
            print(f"🧠 Learned {stats['total_learned']} words")
            print("=" * 70)


if __name__ == "__main__":
    main()
