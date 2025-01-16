from flask import Flask, request, jsonify
from datetime import datetime
import logging
import os
import sys
import json


# Initialize Flask app
app = Flask(__name__)


# Setup logging to a file with rotating handler
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_file = os.path.join(os.path.dirname(__file__), 'access.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=log_format
)


@app.route('/track', methods=['GET'])
def track():
    """Track and log access details for the endpoint."""
    # Get request details
    request_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'referer': request.headers.get('Referer', 'Direct'),
        'timestamp': datetime.now().isoformat(),
        'path': request.path,
        'args': dict(request.args),
        'headers': dict(request.headers),
        'method': request.method,
        'url': request.url,
        'base_url': request.base_url,
    }
    
    # Log the access with detailed data
    logging.info(
        f"Track request received:\n"
        f"URL: {request_data['url']}\n"
        f"IP: {request_data['ip']}\n"
        f"UA: {request_data['user_agent']}\n"
        f"Ref: {request_data['referer']}\n"
        f"Args: {json.dumps(request_data['args'], indent=2)}"
    )
    
    return jsonify({
        'status': 'success',
        'message': 'Access logged successfully',
        'timestamp': request_data['timestamp']
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    # Disable output buffering
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    
    # Run without debug mode and with minimal output
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)