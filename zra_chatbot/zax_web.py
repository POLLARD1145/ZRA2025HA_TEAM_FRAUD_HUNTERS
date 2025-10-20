from flask import Flask, render_template_string, request, jsonify
import requests
import re

app = Flask(__name__)

def clean_response(text):
    """
    Clean and format the AI response by removing markdown formatting,
    asterisks, and ensuring proper plain text formatting.
    """
    if not text:
        return text
    
    # Remove markdown bold (**text**) and other markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    
    # Remove other markdown characters like * at start of lines
    text = re.sub(r'^\s*\*\s*', '', text, flags=re.MULTILINE)
    
    # Remove any remaining isolated asterisks
    text = re.sub(r'\s*\*\s*', ' ', text)
    
    # Clean up table formatting - convert markdown tables to readable format
    lines = text.split('\n')
    cleaned_lines = []
    in_table = False
    
    for line in lines:
        # Skip markdown table separator lines (|---|)
        if re.match(r'^\s*[\|:-]+\s*$', line):
            continue
        
        # Convert table rows to readable format
        if '|' in line and not line.strip().startswith('|'):
            # This might be a table row, clean it up
            line = re.sub(r'\s*\|\s*', ' | ', line.strip())
            cleaned_lines.append(line)
        elif line.strip().startswith('|'):
            # Table row starting with |
            line = re.sub(r'^\|\s*', '', line)
            line = re.sub(r'\s*\|$', '', line)
            line = re.sub(r'\s*\|\s*', ' | ', line)
            cleaned_lines.append(line)
        else:
            # Regular text line
            cleaned_lines.append(line)
    
    # Join lines and clean up extra whitespace
    cleaned_text = '\n'.join(cleaned_lines)
    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)  # Reduce multiple newlines
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Remove extra spaces
    
    return cleaned_text.strip()

HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>ZAX - ZRA Virtual Assistant</title>
<style>
/* minimal trimmed CSS preserving your styles */
body{font-family:Segoe UI,Arial;background:linear-gradient(135deg,#667eea,#764ba2);margin:0;padding:20px;min-height:100vh}
.container{max-width:900px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,0.12)}
.header{background:linear-gradient(135deg,#0066cc,#004499);color:#fff;padding:28px;text-align:center}
.status{padding:12px;text-align:center;background:#d4edda;color:#155724;font-weight:600}
.chat-container{height:420px;overflow-y:auto;padding:20px;background:#f8f9fa}
.message{margin:12px 0;padding:14px;border-radius:14px;max-width:85%;box-shadow:0 2px 8px rgba(0,0,0,0.06);white-space:pre-line}
.bot{background:#fff;margin-right:15%;border:1px solid #e9ecef}
.user{background:linear-gradient(135deg,#0066cc,#004499);color:#fff;margin-left:15%;text-align:right}
.controls{padding:18px;background:#fff;border-top:1px solid #e9ecef;display:flex;flex-direction:column;gap:12px}
.language-selector{display:flex;gap:8px;flex-wrap:wrap}
.language-btn{padding:10px 18px;border-radius:999px;border:2px solid #e9ecef;background:#f8f9fa;cursor:pointer;font-weight:600}
.language-btn.active{background:linear-gradient(135deg,#0066cc,#004499);color:#fff;border-color:#0066cc}
.input-group{display:flex;gap:10px}
input[type="text"]{flex:1;padding:12px 16px;border-radius:20px;border:1px solid #e9ecef}
button.send{padding:12px 20px;border-radius:20px;border:none;background:linear-gradient(135deg,#0066cc,#004499);color:#fff;cursor:pointer;font-weight:700}
.speak-btn{background:none;border:none;color:#0066cc;cursor:pointer;font-size:16px}
.samples{font-size:14px;color:#6c757d;text-align:center}
.audio-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.timestamp{display:block;font-size:11px;color:#777;margin-top:6px}
.speaking{color:#00cc66;}
.voice-info{font-size:12px;color:#666;margin-top:4px;}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🇿🇲 ZAX - ZRA Virtual Assistant</h1>
    <p>Cloud-Powered Multilingual Tax Assistant</p>
  </div>

  <div class="status">✅ Using Cloud AI - Multi-Language Voices Enabled</div>

  <div id="chat" class="chat-container">
    <div class="message bot" id="welcome">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <strong>ZAX</strong>
        <button class="speak-btn" onclick="speakMessage(this, 'Welcome! I speak Bemba, English, and Nyanja. Select a language and ask about TPIN, VAT or deadlines.', 'en')">🔊</button>
      </div>
      <div style="margin-top:8px">Welcome! I speak Bemba, English, and Nyanja. Select your language and ask about taxes, TPIN, VAT, or deadlines.</div>
      <span class="timestamp">Now</span>
    </div>
  </div>

  <div class="controls">
    <div class="language-selector">
      <button class="language-btn active" onclick="setLanguage(event,'en')">English</button>
      <button class="language-btn" onclick="setLanguage(event,'bem')">Bemba</button>
      <button class="language-btn" onclick="setLanguage(event,'nya')">Nyanja</button>
    </div>

    <div class="input-group">
      <input id="userInput" type="text" placeholder="Ask about taxes..." onkeypress="handleKeyPress(event)">
      <button class="send" onclick="sendMessage()">Send</button>
    </div>

    <div class="samples"><strong>Try:</strong> "TPIN registration", "Tax deadlines", "VAT rates"</div>

    <div class="audio-controls">
      <button onclick="stopAllSpeech()">Stop Speech</button>
      <label style="display:flex;align-items:center;gap:6px"><input id="autoSpeak" type="checkbox" onchange="toggleAutoSpeak()"> Auto-speak</label>
      <label>Rate: <select id="voiceRate" onchange="updateVoiceSettings()"><option value="0.9">Slow</option><option value="1.0" selected>Normal</option><option value="1.2">Fast</option></select></label>
      <label>Pitch: <select id="voicePitch" onchange="updateVoiceSettings()"><option value="0.9">Low</option><option value="1.0" selected>Normal</option><option value="1.2">High</option></select></label>
    </div>
    <div class="voice-info" id="currentVoiceInfo">Current voice: English (Default)</div>
  </div>
</div>

<script>
let currentLanguage = 'en';
let autoSpeakEnabled = false;
let voiceSettings = {rate:1.0,pitch:1.0,volume:1.0};
let currentSpeech = null;
let availableVoices = [];

// Enhanced voice preferences for each language with specific female voices
const voicePreferences = {
  'en': [
    // Prefer British English voices for formal tax context
    { keywords: ['Google UK', 'Microsoft David', 'Daniel', 'English (UK)', 'en-GB'], priority: 1 },
    { keywords: ['Google US', 'Microsoft Mark', 'Alex', 'English (US)', 'en-US'], priority: 2 },
    { keywords: ['Samantha', 'Karen', 'Victoria', 'English'], priority: 3 },
    { keywords: ['en-'], priority: 4 } // Any English voice
  ],
  'bem': [
    // Specific female voices for Bemba - Priority to African and warm female voices
    { keywords: ['Tessa', 'Samantha'], priority: 1 }, // Clear, warm female voices
    { keywords: ['Google UK Female', 'Microsoft Zira', 'Karen'], priority: 2 }, // Female British voices
    { keywords: ['Moira', 'Fiona', 'Kate'], priority: 3 }, // Additional female voices
    { keywords: ['African', 'South Africa', 'Kenya', 'Nigeria'], priority: 4 }, // African accents
    { keywords: ['Female', 'Woman'], priority: 5 }, // Any female voice
    { keywords: ['en-'], priority: 6 } // Fallback to any English voice
  ],
  'nya': [
    // Specific female voices for Nyanja - Priority to clear, articulate female voices
    { keywords: ['Tessa', 'Samantha'], priority: 1 }, // Clear, articulate female voices
    { keywords: ['Google UK Female', 'Microsoft Zira', 'Karen'], priority: 2 }, // Female British voices
    { keywords: ['Moira', 'Fiona', 'Kate'], priority: 3 }, // Additional female voices
    { keywords: ['African', 'South Africa', 'Kenya', 'Nigeria'], priority: 4 }, // African accents
    { keywords: ['Female', 'Woman'], priority: 5 }, // Any female voice
    { keywords: ['en-'], priority: 6 } // Fallback to any English voice
  ]
};

// Voice descriptions for display
const voiceDescriptions = {
  'Tessa': 'Warm African female voice',
  'Samantha': 'Clear American female voice', 
  'Google UK Female': 'British female voice',
  'Microsoft Zira': 'Professional female voice',
  'Karen': 'Australian female voice',
  'Moira': 'Irish female voice',
  'Fiona': 'Scottish female voice',
  'Kate': 'British female voice',
  'Google US Female': 'American female voice'
};

function setLanguage(evt,lang){
  currentLanguage = lang;
  document.querySelectorAll('.language-btn').forEach(b=>b.classList.remove('active'));
  evt.target.classList.add('active');
  
  const greet = {
    'en':'Language set to English. How can I help with ZRA services?',
    'bem':'Ululimi lwaya Muchibemba! Bushe Kuti na myafwa shani nangula uku misambilisha pa ma services ya Z R A?',
    'nya':'Chilankhulo chasankhidwa ku Chinyanja! Ndingakuthandizire bwanji pa ma service a ZRA?'
  };
  
  // Update voice info display
  updateVoiceInfo();
  addMessage('bot', greet[lang], false);
}

function updateVoiceInfo() {
  const voiceInfo = document.getElementById('currentVoiceInfo');
  const languageNames = { 'en': 'English', 'bem': 'Bemba', 'nya': 'Nyanja' };
  const selectedVoice = findBestVoice(currentLanguage);
  
  if (selectedVoice) {
    const voiceDesc = voiceDescriptions[selectedVoice.name] || selectedVoice.name;
    voiceInfo.textContent = `Current voice: ${languageNames[currentLanguage]} (${voiceDesc})`;
  } else {
    voiceInfo.textContent = `Current voice: ${languageNames[currentLanguage]} (Default)`;
  }
}

function findBestVoice(language) {
  if (availableVoices.length === 0) return null;
  
  const preferences = voicePreferences[language] || voicePreferences['en'];
  
  // Score each voice based on preferences
  const scoredVoices = availableVoices.map(voice => {
    let score = 0;
    const voiceName = voice.name.toLowerCase();
    const voiceLang = voice.lang.toLowerCase();
    
    for (const pref of preferences) {
      for (const keyword of pref.keywords) {
        if (voiceName.includes(keyword.toLowerCase()) || voiceLang.includes(keyword.toLowerCase())) {
          score = Math.max(score, pref.priority);
          break;
        }
      }
    }
    
    return { voice, score };
  });
  
  // Sort by score (highest first) and return the best
  scoredVoices.sort((a, b) => b.score - a.score);
  return scoredVoices[0]?.score > 0 ? scoredVoices[0].voice : availableVoices[0];
}

function getAvailableFemaleVoices() {
  const femaleVoices = availableVoices.filter(voice => {
    const voiceName = voice.name.toLowerCase();
    return voiceName.includes('female') || voiceName.includes('woman') || 
           voiceName.includes('samantha') || voiceName.includes('tessa') ||
           voiceName.includes('zira') || voiceName.includes('karen') ||
           voiceName.includes('moira') || voiceName.includes('fiona') ||
           voiceName.includes('kate') || voiceName.includes('victoria');
  });
  
  console.log('Available female voices:', femaleVoices.map(v => `${v.name} (${v.lang})`));
  return femaleVoices;
}

function addMessage(sender, text, shouldAutoSpeak=true){
  const chat = document.getElementById('chat');
  const el = document.createElement('div');
  el.className = 'message ' + (sender==='bot'?'bot':'user');
  const id = 'm' + Date.now();
  el.id = id;
  
  if(sender==='bot'){
    // Properly escape text for HTML attributes
    const escapedText = text.replace(/"/g,'&quot;').replace(/'/g,'&#39;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    el.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center">
        <strong>ZAX</strong>
        <button class="speak-btn" data-text="${escapedText}" data-lang="${currentLanguage}">🔊</button>
      </div>
      <div style="margin-top:8px">${text}</div>
      <span class="timestamp">${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</span>
    `;
    chat.appendChild(el);
    
    // Attach speaker action after element is created
    setTimeout(()=>{ 
      const btn = el.querySelector('.speak-btn'); 
      if(btn) {
        btn.addEventListener('click', function() {
          const textToSpeak = this.getAttribute('data-text')
            .replace(/&quot;/g, '"')
            .replace(/&#39;/g, "'")
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>');
          const lang = this.getAttribute('data-lang');
          speakMessage(this, textToSpeak, lang);
        });
        
        // Auto-speak if enabled
        if(shouldAutoSpeak && autoSpeakEnabled) {
          setTimeout(() => {
            const textToSpeak = btn.getAttribute('data-text')
              .replace(/&quot;/g, '"')
              .replace(/&#39;/g, "'")
              .replace(/&lt;/g, '<')
              .replace(/&gt;/g, '>');
            const lang = btn.getAttribute('data-lang');
            speakMessage(btn, textToSpeak, lang);
          }, 500);
        }
      }
    }, 0);
  } else {
    el.innerHTML = `
      <div><strong>You</strong></div>
      <div style="margin-top:8px">${text}</div>
      <span class="timestamp">${new Date().toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}</span>
    `;
    chat.appendChild(el);
  }
  chat.scrollTop = chat.scrollHeight;
}

function initSpeechSupported(){ 
  return 'speechSynthesis' in window; 
}

function loadVoices() {
  availableVoices = speechSynthesis.getVoices();
  console.log('Available voices:', availableVoices.map(v => `${v.name} (${v.lang})`));
  
  // Log available female voices for debugging
  const femaleVoices = getAvailableFemaleVoices();
  console.log('Available female voices for Bemba/Nyanja:', femaleVoices.map(v => v.name));
  
  updateVoiceInfo();
}

function speakMessage(button, text, language = currentLanguage){
  stopAllSpeech();
  if(!initSpeechSupported()){ 
    alert('Text-to-speech not supported in this browser. Please use Chrome, Edge, or Safari.'); 
    return; 
  }
  
  button.classList.add('speaking'); 
  button.innerText = '⏸️';
  
  currentSpeech = new SpeechSynthesisUtterance(text);
  currentSpeech.rate = voiceSettings.rate; 
  currentSpeech.pitch = voiceSettings.pitch; 
  currentSpeech.volume = voiceSettings.volume;
  
  // Find the best voice for the current language
  const bestVoice = findBestVoice(language);
  if (bestVoice) {
    currentSpeech.voice = bestVoice;
    console.log(`Using voice for ${language}:`, bestVoice.name, bestVoice.lang);
  }
  
  currentSpeech.onend = ()=>{ 
    button.classList.remove('speaking'); 
    button.innerText='🔊'; 
    currentSpeech=null; 
  };
  
  currentSpeech.onerror = (event)=>{ 
    console.error('Speech synthesis error:', event);
    button.classList.remove('speaking'); 
    button.innerText='🔊'; 
    currentSpeech=null; 
  };
  
  speechSynthesis.speak(currentSpeech);
  
  // Toggle behavior on click
  button.onclick = ()=>{ 
    if(speechSynthesis.speaking && !speechSynthesis.paused) {
      speechSynthesis.cancel();
    } else {
      const textToSpeak = button.getAttribute('data-text')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>');
      const lang = button.getAttribute('data-lang');
      speakMessage(button, textToSpeak, lang);
    }
  };
}

function stopAllSpeech(){
  if('speechSynthesis' in window) {
    speechSynthesis.cancel();
  }
  document.querySelectorAll('.speak-btn').forEach(b=>{ 
    b.classList.remove('speaking'); 
    b.innerText='🔊'; 
    b.onclick = function() {
      const textToSpeak = this.getAttribute('data-text')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'")
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>');
      const lang = this.getAttribute('data-lang');
      speakMessage(this, textToSpeak, lang);
    };
  });
  currentSpeech = null;
}

function toggleAutoSpeak(){ 
  autoSpeakEnabled = document.getElementById('autoSpeak').checked; 
}

function updateVoiceSettings(){ 
  voiceSettings.rate = parseFloat(document.getElementById('voiceRate').value); 
  voiceSettings.pitch = parseFloat(document.getElementById('voicePitch').value); 
}

function sendMessage(){
  const input = document.getElementById('userInput');
  const message = input.value.trim();
  if(!message) return;
  
  addMessage('user', message, false);
  input.value = '';
  
  // Show typing indicator
  const typing = document.createElement('div'); 
  typing.className='message bot'; 
  typing.id='typing'; 
  typing.innerHTML='<div><strong>ZAX</strong></div><div style="margin-top:8px">Thinking...</div>'; 
  document.getElementById('chat').appendChild(typing);
  chat.scrollTop = chat.scrollHeight;
  
  fetch('/chat', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({message:message, language: currentLanguage})
  })
  .then(r=>r.json())
  .then(data=>{
    const t = document.getElementById('typing'); 
    if(t) t.remove();
    addMessage('bot', data.response || 'Sorry, no reply from service.', true);
  })
  .catch(err=>{
    const t = document.getElementById('typing'); 
    if(t) t.remove();
    addMessage('bot', 'Service error: please check your internet connection and ensure Ollama is running.', false);
  });
}

function handleKeyPress(e){ 
  if(e.key==='Enter') sendMessage(); 
}

// Initialize on load
document.addEventListener('DOMContentLoaded', ()=>{ 
  document.getElementById('userInput').focus(); 
  if(initSpeechSupported()) {
    // Load voices and set up voice change listener
    loadVoices();
    speechSynthesis.onvoiceschanged = loadVoices;
  }
});
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        payload = request.get_json(force=True)
        user_message = (payload.get('message') or '').strip()
        language = (payload.get('language') or 'en').lower()

        if not user_message:
            return jsonify({'response': 'Please type a question first.'})

        prompts = {
            'en': """You are ZAX - the Zambia Revenue Authority virtual assistant. Help taxpayers in English.

KEY TAX INFORMATION:
- TPIN registration: Required for all, register at ZRA office with NRC and proof of address
- Tax deadlines: Individual returns June 30, Corporate returns March 31, VAT returns 21st monthly
- VAT: 16% rate, registration required for businesses over 800,000 ZMW turnover
- Penalties: Late filing 500 ZMW, late payment 10% + interest
- Payment: Online portal, bank transfers, ZRA offices

Always respond in English. Be accurate and helpful. Format your response in clean, readable text without markdown formatting, asterisks, or special characters.""",

            'bem': """You are ZAX - Zambia Revenue Authority virtual assistant. You help taxpayers in Bemba.

IFYO MULANGA:
- UKupangisha TPIN: Fyaishila kuli bantu bonse, Kabiyeni ku ofesi ya ZRA na NRC Yenu..kabili Na Address Yapanchende epo mwikala
- Ubushiku ebo mufwie Ukulipila TAX: Umuntu atemwa eka ni pa 30 June, Akampani ni pa 31 March, Elo na VAT nayena ni pa 21 wa muweshi
- VAT: Ni 16%, ifyakupandisha fyafulwa pa mabizinesi ayasambilila ukutula ZMW 800,000
- Ifilondwa: Ukulemba cilya - ZMW 500, ukulipila cilya - 10% + ndalama shacilendo
- Indalama: Pa ZRA online, ukutuma ku bank, ku ofesi sha ZRA

Pusheni mu Cibemba. Ba helpful na accurate. Landa ifyakupandisha mwa bulangeti bwabwino, tafyalilamo asterisks kapena fyacimanyilo.""",

            'nya': """You are ZAX - Zambia Revenue Authority virtual assistant. You help taxpayers in Nyanja.

ZOTHANDIZA:
- Kulembetsa TPIN: Zofunika kwa onse, lembetsani ku ofesi ya ZRA ndi NRC ndi chizindikiro cha malo
- Nthawi zofalitsa: Anthu pa 30 June, Makampani pa 31 March, VAT pa 21 wa mwezi uliwonse
- VAT: 16%, kulembetsa kofunika kwa mabizinesi opitilira ZMW 800,000
- Zipemo: Kulembetsa mochedwa - ZMW 500, Kulipira mochedwa - 10% + ndalama zina
- Malipiro: Pa ZRA online, kutumiza ku bank, ku maofesi a ZRA

Yankhani mu Chinyanja. Khalani othandiza ndi oona. Perekani yankho losafalitsa m'mene lili clean, losalembedwa m'makalata kapena zizindikiro zina."""
        }

        prompt = f"{prompts.get(language, prompts['en'])}\n\nUser: {user_message}"

        # Call Ollama cloud model
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:20b-cloud", 
                "prompt": prompt, 
                "stream": False
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if resp.status_code != 200:
            return jsonify({'response': '⚠️ The AI service is currently unavailable. Please ensure Ollama is running and try again later.'})

        data = resp.json()
        bot_text = data.get('response')
        
        if not bot_text:
            bot_text = "I apologize, but I couldn't generate a response. Please try again."

        # Clean the response before sending to frontend
        cleaned_response = clean_response(bot_text)
        
        return jsonify({'response': cleaned_response})

    except requests.exceptions.RequestException as re:
        return jsonify({'response': f'Connection error: Please ensure Ollama is running with "ollama serve". ({str(re)})'})
    except Exception as e:
        return jsonify({'response': f'Unexpected error: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting ZAX Cloud Interface...")
    print("📧 Open: http://localhost:5000")
    print("🔊 Multi-Language Voices Enabled")
    print("🗣️  Dedicated female voices for Bemba and Nyanja")
    print("👩  Bemba: Tessa, Samantha, Zira, Karen")
    print("👩  Nyanja: Tessa, Samantha, Moira, Fiona") 
    print("☁️  Using Cloud AI Model")
    print("✨ Response Cleaning Enabled - No more asterisks!")
    app.run(debug=True, host='0.0.0.0', port=5000)