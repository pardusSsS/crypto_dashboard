from flask import Flask, jsonify, render_template
#from flask_cors import CORS
import logging
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase
cred = credentials.Certificate('./firebase_config.json')
initialize_app(cred)
db = firestore.client()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    #CORS(app)
    
    @app.route('/')
    def index():
        """Render dashboard page"""
        return render_template('index.html')
    
    @app.route('/disclaimer')
    def disclaimer():
        """Render disclaimer page"""
        return render_template('disclaimer.html')
    
    @app.route('/api/status')
    def get_status():
        """Get bot status from Firestore"""
        try:
            status_doc = db.collection('bot_status').document('current').get()
            if status_doc.exists:
                return jsonify(status_doc.to_dict())
            return jsonify({
                'status': 'unknown',
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Error getting status from Firestore: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/portfolio')
    def get_portfolio():
        """Get portfolio information from Firestore"""
        try:
            portfolio_doc = db.collection('portfolio').document('current').get()
            if portfolio_doc.exists:
                return jsonify(portfolio_doc.to_dict())
            return jsonify({
                'balance': {
                    'total': 0.0,
                    'available': 0.0,
                    'pnl': 0.0
                },
                'active_positions': 0
            })
        except Exception as e:
            logger.error(f"Error getting portfolio from Firestore: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/signals')
    def get_signals():
        """Get trading signals from Firestore"""
        try:
            signals_doc = db.collection('signals').document('current').get()
            if signals_doc.exists:
                return jsonify(signals_doc.to_dict())
            return jsonify({})
        except Exception as e:
            logger.error(f"Error getting signals from Firestore: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    return app

if __name__ == '__main__':
    try:
        logger.info("Creating Flask app...")
        app = create_app()
        
        logger.info("Starting Flask server...")
        #app.run(port=5002, debug=True)
        app.run(host='0.0.0.0', port=8000, debug=True)

    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise 