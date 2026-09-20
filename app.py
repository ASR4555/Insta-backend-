from flask import Flask, request, jsonify
from flask_cors import CORS
import instaloader

app = Flask(__name__)
# CORS allow karna zaroori hai taaki Netlify hamare server se baat kar sake
CORS(app)

L = instaloader.Instaloader()

@app.route('/api/search', methods=['GET'])
def search_teacher():
    # Netlify search bar se username lena
    username = request.args.get('username')
    
    if not username:
        return jsonify({"status": "error", "message": "Username zaroori hai!"}), 400
        
    try:
        # Instagram se profile data fetch karna
        profile = instaloader.Profile.from_username(L.context, username)
        
        if profile.is_private:
            return jsonify({"status": "error", "message": "Yeh account private hai. Sirf public accounts allowed hain."}), 200
            
        feed_data = {
            "teacher_name": profile.full_name,
            "username": profile.username,
            "posts": []
        }
        
        # Sirf sabse naye 6 posts/reels nikalna
        for count, post in enumerate(profile.get_posts()):
            if count >= 6:
                break
            
            post_info = {
                "caption": post.caption if post.caption else "Educational Post",
                "date": str(post.date_utc),
                "is_video": post.is_video,
                "media_url": post.video_url if post.is_video else post.url
            }
            feed_data["posts"].append(post_info)
            
        return jsonify({"status": "success", "data": feed_data}), 200

    except instaloader.exceptions.ProfileNotExistsException:
        return jsonify({"status": "error", "message": "Teacher ka username galat hai."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Server par koi dikkat aayi: {str(e)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
