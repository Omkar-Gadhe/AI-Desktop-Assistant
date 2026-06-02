<!-- # AI-Desktop-Assistant -->
<!-- AI Desktop Assistant (Python), This project started with a simple idea — what if a desktop assistant could do more than just reply like a chatbot?  Built in Python, this AI Desktop Assistant is my attempt to create a system that can talk, understand commands, and automate useful desktop tasks. -->
<!-- <br> -->
<div align="center">
  <h1>👻 Ghost AI</h1>
  <p><strong>A Modular, Terminal-Based Desktop Assistant powered by Gemini</strong></p>
  <p><em>Status: Operational & Evolving (Active Development as of June 2026)</em></p>
</div>

<hr />

<h2>🚀 Overview</h2>
<p>
  Ghost AI is a lightweight, ultra-fast, modular terminal assistant powered by the Gemini API. 
  Built with a decoupled architecture, it splits intellectual conversational capabilities from local system execution, 
  allowing it to chat, handle deep reasoning tasks, and spawn native desktop applications seamlessly on your Linux machine.
</p>

<hr />

<h2>🎯 Key Features</h2>
<ul>
  <li>
    <strong>Smart Dual-Engine Routing:</strong>
    <ul>
      <li><em>Fast Mode:</em> Standard lightning-fast streaming text responses using Gemini Flash.</li>
      <li><em>Deep Thinking Mode:</em> Prepending a prompt with <code>/think</code> dynamically reroutes the request to a high-reasoning model pipeline.</li>
    </ul>
  </li>
  <li>
    <strong>Sliding-Window Memory:</strong> Keeps conversation contextual without exploding API costs. Implements a bounded short-term memory system that caps history payload sizes to a maximum of 3 turns.
  </li>
  <li>
    <strong>Local Application Spawning:</strong> Completely token-free intent detection intercepts commands like <code>open firefox</code> or <code>run vs code</code> to launch native applications instantly using background sub-processes without freezing your terminal conversation.
  </li>
  <li>
    <strong>Network Resilience:</strong> Features robust error handling with automatic exponential backoff retry loops to smoothly handle server-side rate limits or service hiccups.
  </li>
  <li>
    <strong>Clean Architectural Separation:</strong> Built using single-responsibility principles where components are completely decoupled across isolated files:
    <ul>
      <li><code>chatbot.py</code>: High-level workflow orchestration and main runtime loop.</li>
      <li><code>ai_gateway.py</code>: Network communication and API streaming pipelines.</li>
      <li><code>history.py</code>: Structured memory context and sliding-window management.</li>
      <li><code>act_brain.py</code>: Local OS command execution and hardware application tracking.</li>
    </ul>
  </li>
</ul>

<hr />

<h2>🛠️ System Architecture Diagram</h2>
<pre>
                 [ User Input Terminal ]
                           │
                    (Intent Detection)
                     /           \
         [ Chat Intent ]       [ App Launch Intent ]
               │                          │
        (Memory Logging)            (Zero-Token Bypass)
               │                          │
    [ Network / Retry Guard ]       [ Local Subprocess ]
               │                          │
     [ Gemini Stream API ]         🚀 Launches Application
               │
        (Stream Append)
               │
         [ UI Render ]
</pre>

<hr />

<h2>🏃‍♂️ Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.10+</li>
  <li>Fedora Linux (or any Linux distribution with <code>subprocess</code> access to app binaries)</li>
  <li>A Google AI Studio API Key</li>
</ul>

<h3>Installation & Launch</h3>
<ol>
  <li>Clone the repository to your local machine.</li>
  <li>
    Set your Google API key as an environment variable:
    <pre><code>export GEMINI_API_KEY="your-api-key-here"</code></pre>
  </li>
  <li>
    Run the application:
    <pre><code>python chatbot.py</code></pre>
  </li>
</ol>

<hr />

<h2>🔮 Future Roadmap</h2>
<p>Project Ghost is built to adapt. Upcoming structural updates include:</p>
<ul>
  <li><strong>Persistent Local Memory:</strong> Transitioning from volatile RAM-based storage to a local SQLite or JSON tracking layer to remember history across machine reboots without altering online API payload costs.</li>
  <li><strong>Dynamic Command Mapping:</strong> Eliminating hardcoded application dictionaries by utilizing semantic matching for broader system utilities.</li>
  <li><strong>Voice Interfacing:</strong> Adding local Text-to-Speech (TTS) and Speech-to-Text (STT) streams directly into the modular gateway pipeline.</li>
  <li><strong>GUI HUD Overlay:</strong> Graduating from the terminal environment into an elegant, minimalist desktop widget system.</li>
</ul>