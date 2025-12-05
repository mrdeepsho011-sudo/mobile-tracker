from flask import Flask, request, jsonify, render_template_string
import requests
import threading
import webbrowser
import time

app = Flask(__name__)

# ================= HTML TEMPLATE =================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Mobile Number Tracker - cyber deep</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:white;font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;min-height:100vh;padding:20px;}
        .glass-box{max-width:750px;background:white;margin:20px auto;padding:30px;border-radius:20px;border:1px solid #ddd;}
        .header{text-align:center;margin-bottom:30px;}
        .header h2{color:black;font-size:2.2em;margin-bottom:10px;font-weight:700;}
        .header p{color:#444;font-size:1.1em;}
        .input-group{margin-bottom:25px;}
        .input-group input{width:100%;padding:18px 20px;background:white;border:2px solid #bbb;border-radius:15px;font-size:18px;color:black;}
        .glow-button{width:100%;padding:18px;background:black;border:none;border-radius:15px;color:white;font-size:18px;cursor:pointer;}
        .loader{display:none;margin:25px auto;width:60px;height:60px;border:4px solid #ccc;border-top:4px solid black;border-radius:50%;animation:spin 1s linear infinite;}
        @keyframes spin{100%{transform:rotate(360deg);}}
        #info{margin-top:25px;font-size:15px;background:#f8f9fa;padding:25px;border-radius:15px;display:none;color:black;border:1px solid #ddd;}
        .success-message,.error-message{padding:15px;border-radius:10px;margin-top:20px;display:none;font-size:17px;}
        .success-message{background:#d4edda;color:#155724;}
        .error-message{background:#f8d7da;color:#721c24;}
        .info-item{margin:12px 0;padding:12px;background:white;border-radius:8px;border-left:4px solid #007bff;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
        .info-header{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:15px;border-radius:10px;margin-bottom:20px;text-align:center;}
    </style>
</head>
<body>

<div class="glass-box">
    <div class="header">
        <h2>Mobile Number Tracker</h2>
        <p>Powered by cyber deep</p>
    </div>
    <div class="input-group">
        <input id="mobile" placeholder="Enter mobile number (e.g. 6294782049)">
    </div>
    <button class="glow-button" onclick="startTrack()">Track Now</button>
    <div id="loader" class="loader"></div>
    
    <div id="success" class="success-message"></div>
    <div id="error" class="error-message"></div>
    <div id="info"></div>
</div>

<script>
function startTrack(){
    let mobile=document.getElementById("mobile").value.trim();
    if(mobile.length<10 || isNaN(mobile)){
        showError("Please enter a valid mobile number (only digits, min 10)");
        return;
    }
    document.getElementById("loader").style.display="block";
    document.getElementById("info").style.display="none";
    document.getElementById("error").style.display="none";
    document.getElementById("success").style.display="none";

    fetch('/track?mobile='+encodeURIComponent(mobile))
    .then(res=>res.json())
    .then(apiData=>{
        document.getElementById("loader").style.display="none";
        if(!apiData.success){
            showError(apiData.error||"No information found");
            return;
        }
        showSuccess("✅ Information found successfully!");
        displayInfo(mobile,apiData.data);
    })
    .catch(err=>{
        document.getElementById("loader").style.display="none";
        showError("❌ Error: "+err.message);
    });
}

function displayInfo(mobile,data){
    let infoHTML=`<div class="info-header"><h3>📱 MOBILE INFORMATION</h3></div>
    <div class="info-item"><strong>Target Mobile:</strong> ${mobile}</div>`;
    
    for(let key in data){
        if(data[key]!==null && data[key]!=="" && data[key]!=="NA" && data[key]!=="N/A"){
            infoHTML+=`<div class="info-item"><strong>${key.replace(/_/g," ").toUpperCase()}:</strong> ${data[key]}</div>`;
        }
    }

    document.getElementById("info").innerHTML=infoHTML;
    document.getElementById("info").style.display="block";
}

function showSuccess(msg){document.getElementById("success").innerText=msg;document.getElementById("success").style.display="block";}
function showError(msg){document.getElementById("error").innerText=msg;document.getElementById("error").style.display="block";}
window.onload=function(){document.getElementById("mobile").addEventListener("keypress",e=>{if(e.key==="Enter")startTrack();});}
</script>

</body>
</html>
'''

# ================= BACKEND ROUTES =================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/track')
def track():
    mobile=request.args.get('mobile','').strip()
    if not mobile.isdigit() or len(mobile)<10:
        return jsonify({"success":False,"error":"Invalid mobile number"}),400

    try:
        api_url=f"https://hitackgrop.vercel.app/get_data?mobile={mobile}&key=Demo"
        resp=requests.get(api_url,timeout=20)
        resp.raise_for_status()

        raw=resp.json()
        result=raw["data"]["data"]["result"][0]

        return jsonify({"success":True,"data":result})

    except requests.exceptions.HTTPError as e:
        if resp.status_code==429:
            return jsonify({"success":False,"error":"Too many requests, try later"}),429
        return jsonify({"success":False,"error":f"HTTP error: {e}"}),500

    except Exception as e:
        return jsonify({"success":False,"error":f"Server error: {e}"}),500

def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__=="__main__":
    print("🚀 Mobile Tracker Starting...")
    print("🌐 Open: http://127.0.0.1:5000")
    threading.Thread(target=open_browser,daemon=True).start()
    app.run(host="127.0.0.1",port=5000,debug=False)