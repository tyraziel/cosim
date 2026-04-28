"""Single-page HTML/CSS/JS template for the web UI."""

WEB_UI = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CoSim</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/js-yaml@4/dist/js-yaml.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  /* -- Theme System -- */
  :root {
    --bg: #1a1a2e;
    --panel: #16213e;
    --sidebar: #121a30;
    --border: #0f3460;
    --border-mid: #1a1a2e;
    --border-dark: #333;
    --input-bg: #111;
    --accent: #e94560;
    --accent-dark: #c0392b;
    --text: #e0e0e0;
    --text-dim: #888;
    --text-dimmer: #555;
    --text-bright: #fff;
    --highlight: #4fc3f7;
  }
  [data-theme="stadium"] {
    --bg: #000000;
    --panel: #0d0d0d;
    --sidebar: #050505;
    --border: #2a2a2a;
    --border-mid: #1a1a1a;
    --border-dark: #1a1a1a;
    --input-bg: #111111;
    --accent: #00e5ff;
    --accent-dark: #00b8cc;
    --text: #ffffff;
    --text-dim: #aaaaaa;
    --text-dimmer: #666666;
    --text-bright: #ffffff;
    --highlight: #ffeb3b;
  }
  [data-theme="field"] {
    --bg: #0a1a0a;
    --panel: #0f200f;
    --sidebar: #081408;
    --border: #1e4d1e;
    --border-mid: #162816;
    --border-dark: #1e3a1e;
    --input-bg: #071207;
    --accent: #f5a623;
    --accent-dark: #d4891a;
    --text: #e8f0e8;
    --text-dim: #7a9e7a;
    --text-dimmer: #4a6a4a;
    --text-bright: #ffffff;
    --highlight: #7dff8a;
  }
  [data-theme="solarized-dark"] {
    --bg: #002b36;
    --panel: #073642;
    --sidebar: #002029;
    --border: #586e75;
    --border-mid: #073642;
    --border-dark: #2a4a52;
    --input-bg: #003847;
    --accent: #cb4b16;
    --accent-dark: #a83c11;
    --text: #839496;
    --text-dim: #657b83;
    --text-dimmer: #586e75;
    --text-bright: #93a1a1;
    --highlight: #2aa198;
  }
  [data-theme="solarized-light"] {
    --bg: #fdf6e3;
    --panel: #eee8d5;
    --sidebar: #f5efdc;
    --border: #93a1a1;
    --border-mid: #eee8d5;
    --border-dark: #d3cbb7;
    --input-bg: #fff8e7;
    --accent: #cb4b16;
    --accent-dark: #a83c11;
    --text: #657b83;
    --text-dim: #839496;
    --text-dimmer: #93a1a1;
    --text-bright: #073642;
    --highlight: #268bd2;
  }

  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; }

  /* -- Header with tabs -- */
  #header { background: var(--panel); padding: 0 20px; border-bottom: 1px solid var(--border);
            display: flex; align-items: stretch; gap: 0; }
  #header h1 { font-size: 18px; color: var(--accent); display: flex; align-items: center; padding: 12px 16px 12px 0;
               border-right: 1px solid var(--border); margin-right: 0; }
  .header-tab { padding: 12px 20px; font-size: 13px; font-weight: 600; cursor: pointer;
                background: transparent; border: none; color: var(--text-dim);
                border-bottom: 2px solid transparent; transition: all 0.15s ease; }
  .header-tab:hover { color: var(--text); }
  .header-tab.active { color: var(--accent); border-bottom-color: var(--accent); }
  #session-controls { margin-left: auto; display: flex; align-items: center; gap: 6px; padding: 8px 0; }
  .session-btn { background: transparent; color: var(--text-dim); border: 1px solid var(--border-dark); padding: 6px 12px;
                 border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: 600; }
  .session-btn:hover { border-color: var(--accent); color: var(--accent); }
  #session-load-select { background: var(--bg); color: var(--text-dim); border: 1px solid var(--border-dark); padding: 6px 8px;
                         border-radius: 6px; font-size: 12px; max-width: 200px; }
  #orch-status { display: flex; align-items: center; gap: 5px; margin-right: 8px;
                 padding: 4px 10px; border: 1px solid var(--border-dark); border-radius: 6px; }
  #orch-label { font-size: 11px; color: var(--text-dim); }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
  .status-dot.disconnected { background: #666; }
  .status-dot.waiting { background: #f39c12; }
  .status-dot.connecting { background: #f39c12; animation: pulse 1s ease-in-out infinite; }
  .status-dot.starting { background: #f39c12; animation: pulse 1s ease-in-out infinite; }
  .status-dot.ready { background: #2ecc71; }
  .status-dot.responding { background: #3498db; animation: pulse 0.5s ease-in-out infinite; }
  .status-dot.restarting { background: #e94560; animation: pulse 0.8s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

  /* -- NPCs tab -- */
  #npcs-pane { padding: 0; flex-direction: row; }
  #npcs-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                  display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  #npcs-main { flex: 1; overflow-y: auto; padding: 20px; }
  #npcs-content { max-width: 1000px; }
  #npcs-empty { color: var(--text-dimmer); text-align: center; padding: 40px; }
  .npc-tier-section { margin-bottom: 24px; }
  .npc-tier-header { font-size: 13px; font-weight: 700; text-transform: uppercase;
                     letter-spacing: 1px; color: var(--text-dim); margin-bottom: 10px;
                     padding-bottom: 6px; border-bottom: 1px solid var(--border-dark); }
  .npc-tier-grid { display: flex; flex-wrap: wrap; gap: 12px; }
  .npc-card { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 10px;
              padding: 14px 16px; flex: 1 1 160px; max-width: 220px; min-width: 160px;
              transition: border-color 0.15s; }
  .npc-card:hover { border-color: var(--text-dimmer); }
  .npc-card.offline { opacity: 0.6; }
  .npc-card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
  .npc-status-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .npc-status-dot.ready { background: #2ecc71; }
  .npc-status-dot.starting { background: #f39c12; animation: pulse 1s ease-in-out infinite; }
  .npc-status-dot.responding { background: #3498db; animation: pulse 0.5s ease-in-out infinite; }
  .npc-status-dot.writing-docs { background: #9b59b6; animation: pulse 0.8s ease-in-out infinite; }
  .npc-status-dot.committing-code { background: #e67e22; animation: pulse 0.8s ease-in-out infinite; }
  .npc-status-dot.managing-tickets { background: #1abc9c; animation: pulse 0.8s ease-in-out infinite; }
  .npc-status-dot.processing-commands { background: #f39c12; animation: pulse 0.8s ease-in-out infinite; }
  .npc-status-dot.firing { background: #e94560; animation: pulse 1.5s ease-in-out infinite; }
  .npc-status-dot.offline { background: #666; }
  .npc-status-dot.disconnected { background: #444; }
  .npc-status-dot.unknown { background: #444; }
  .npc-card-state { font-size: 10px; color: var(--text-dimmer); margin-left: auto; }
  .npc-card-name { font-size: 14px; font-weight: 700; color: var(--text); }
  .npc-card-desc { font-size: 11px; color: var(--text-dim); margin-bottom: 8px; line-height: 1.4; }
  .npc-card-section-label { font-size: 10px; font-weight: 600; text-transform: uppercase;
                           letter-spacing: 0.5px; color: var(--text-dimmer); margin-bottom: 3px; margin-top: 6px; }
  .npc-card-tags { margin-bottom: 4px; line-height: 1.8; }
  .npc-tag { background: var(--input-bg); color: var(--text-dim); padding: 1px 6px; border-radius: 4px; font-size: 11px;
             margin-right: 3px; display: inline-block; }
  .npc-tag-folder { border-left: 2px solid #3498db; }
  .npc-toggle-btn { width: 100%; background: transparent; border: 1px solid var(--border-dark);
                    color: var(--text-dim); padding: 5px; border-radius: 6px; font-size: 11px;
                    cursor: pointer; transition: all 0.15s; }
  .npc-toggle-btn:hover { border-color: var(--accent); color: var(--accent); }
  .npc-toggle-btn.is-online:hover { border-color: #f39c12; color: #f39c12; }
  .npc-detail-tab { transition: all 0.15s; }
  .npc-detail-tab.active { background: var(--accent); border-color: var(--accent); color: var(--text-bright); }
  .npc-config-check { display: flex; align-items: center; gap: 4px; background: var(--bg);
                      padding: 4px 10px; border-radius: 6px; border: 1px solid var(--border-dark);
                      font-size: 12px; color: var(--text-dim); cursor: pointer; }
  .npc-config-check:hover { border-color: var(--text-dimmer); }
  .npc-config-check input { accent-color: #e94560; }
  .npc-config-check.checked { color: var(--text); border-color: var(--text-dimmer); }
  .thought-item { padding: 8px 12px; cursor: pointer; border-bottom: 1px solid var(--bg);
                  font-size: 11px; color: var(--text-dim); transition: background 0.1s; }
  .thought-item:hover { background: var(--border-mid); }
  .thought-item.active { background: var(--border-mid); color: var(--text); border-left: 3px solid var(--accent); }
  .thought-item-time { color: var(--text-dimmer); font-size: 10px; }
  .thought-item-preview { color: var(--text-dim); margin-top: 2px; overflow: hidden;
                          text-overflow: ellipsis; white-space: nowrap; }

  /* -- Usage tab -- */
  #usage-pane { padding: 0; flex-direction: row; }
  #usage-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                   display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  .usage-sidebar-section { font-size: 11px; font-weight: 700; text-transform: uppercase;
                           letter-spacing: 1px; color: var(--text-dimmer); padding: 10px 14px 4px; }
  .usage-stat { padding: 4px 14px; font-size: 12px; color: var(--text-dim); }
  .usage-stat strong { color: var(--text); }
  #usage-main { flex: 1; overflow-y: auto; padding: 20px; }
  #usage-content { max-width: 1000px; }
  #usage-empty { color: var(--text-dimmer); text-align: center; padding: 40px; }
  .usage-grid { display: flex; flex-wrap: wrap; gap: 12px; }
  .usage-card { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 10px;
                padding: 14px 16px; flex: 1 1 200px; max-width: 280px; min-width: 200px;
                transition: border-color 0.15s; }
  .usage-card:hover { border-color: var(--text-dimmer); }
  .usage-card-name { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 10px;
                     padding-bottom: 6px; border-bottom: 1px solid var(--border-dark); }
  .usage-card-row { display: flex; justify-content: space-between; padding: 3px 0;
                    font-size: 12px; color: var(--text-dim); }
  .usage-card-row .label { color: var(--text-dimmer); }
  .usage-card-row .value { color: var(--text); font-weight: 600; font-family: monospace; }
  .usage-card-row .value.cost { color: #2ecc71; }

  /* -- Advanced tab -- */
  #advanced-pane { padding: 0; }

  /* -- Recap tab -- */
  #recap-pane { padding: 0; flex-direction: row; }
  #recap-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                   display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  #recap-main { flex: 1; overflow-y: auto; }
  .recap-item { padding: 8px 14px; cursor: pointer; border-bottom: 1px solid var(--bg);
                font-size: 12px; color: var(--text-dim); transition: background 0.1s; }
  .recap-item:hover { background: var(--border-mid); }
  .recap-item.active { background: var(--border-mid); color: var(--text); border-left: 3px solid var(--accent); }
  .recap-item-style { font-weight: 600; color: var(--highlight); }
  .recap-item-time { font-size: 10px; color: var(--text-dimmer); margin-top: 2px; }

  /* -- Email tab -- */
  #email-pane { padding: 0; flex-direction: row; }
  #email-sidebar { width: 300px; min-width: 300px; background: var(--sidebar); border-right: 1px solid var(--border);
                   display: flex; flex-direction: column; overflow: hidden; }
  #email-main { flex: 1; overflow-y: auto; padding: 20px; }
  .email-item { padding: 10px 12px; border-bottom: 1px solid var(--bg); cursor: pointer; transition: background 0.1s; }
  .email-item:hover { background: var(--border-mid); }
  .email-item.active { background: var(--border-mid); border-left: 3px solid #3498db; }
  .email-item-from { font-size: 12px; font-weight: 700; color: var(--highlight); }
  .email-item-subject { font-size: 13px; color: var(--text); margin-top: 2px; overflow: hidden;
                        text-overflow: ellipsis; white-space: nowrap; }
  .email-item-date { font-size: 10px; color: var(--text-dimmer); margin-top: 2px; }

  /* -- Memos tab -- */
  #memos-pane { padding: 0; flex-direction: row; }
  #memos-sidebar { width: 300px; min-width: 300px; background: var(--sidebar); border-right: 1px solid var(--border);
                   display: flex; flex-direction: column; overflow: hidden; }
  #memos-main { flex: 1; overflow-y: auto; padding: 20px; }
  .memo-thread-item { padding: 10px 12px; border-bottom: 1px solid var(--bg); cursor: pointer; transition: background 0.1s; }
  .memo-thread-item:hover { background: var(--border-mid); }
  .memo-thread-item.active { background: var(--border-mid); border-left: 3px solid #2ecc71; }
  .memo-thread-title { font-size: 13px; font-weight: 700; color: var(--text); }
  .memo-thread-preview { font-size: 11px; color: var(--text-dimmer); margin-top: 4px; overflow: hidden;
                         text-overflow: ellipsis; white-space: nowrap; }
  .memo-thread-meta { font-size: 10px; color: var(--text-dimmer); margin-top: 2px; }
  .memo-post { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px; padding: 14px; margin-bottom: 10px; }
  .memo-post-author { font-size: 12px; font-weight: 700; color: var(--highlight); }
  .memo-post-date { font-size: 10px; color: var(--text-dimmer); margin-left: 8px; }
  .memo-post-text { font-size: 13px; color: var(--text); margin-top: 8px; line-height: 1.5; }
  .memo-post-text p { margin: 0 0 8px 0; }
  .memo-post-text p:last-child { margin-bottom: 0; }
  .memo-post-text ul, .memo-post-text ol { margin: 4px 0 8px 20px; padding: 0; }
  .memo-post-text pre { background: var(--input-bg); padding: 8px 10px; border-radius: 4px; overflow-x: auto; margin: 8px 0; }
  .memo-post-text code { background: var(--input-bg); padding: 1px 4px; border-radius: 3px; font-size: 12px; }
  .memo-post-text pre code { background: none; padding: 0; }
  .memo-post-text h1, .memo-post-text h2, .memo-post-text h3, .memo-post-text h4 { margin: 12px 0 6px 0; color: var(--text-bright); }
  .memo-post-text blockquote { border-left: 3px solid var(--border-dark); margin: 8px 0; padding: 4px 12px; color: var(--text-dim); }
  .memo-post-text table { border-collapse: collapse; margin: 8px 0; }
  .memo-post-text th, .memo-post-text td { border: 1px solid var(--border-dark); padding: 4px 8px; font-size: 12px; }

  /* -- Blog tab -- */
  #blog-pane { padding: 0; flex-direction: row; }
  #blog-sidebar { width: 300px; min-width: 300px; background: var(--sidebar); border-right: 1px solid var(--border);
                  display: flex; flex-direction: column; overflow: hidden; }
  #blog-main { flex: 1; overflow-y: auto; padding: 20px; }
  .blog-filter-bar { display: flex; gap: 4px; padding: 8px 10px; border-bottom: 1px solid var(--border-dark); }
  .blog-filter-btn { flex: 1; background: transparent; border: 1px solid var(--border-dark); color: var(--text-dim);
                     padding: 4px 8px; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; }
  .blog-filter-btn.active { background: var(--accent); border-color: var(--accent); color: var(--text-bright); }
  .blog-post-item { padding: 10px 12px; border-bottom: 1px solid var(--border-mid); cursor: pointer; transition: background 0.1s; }
  .blog-post-item:hover { background: var(--border-mid); }
  .blog-post-item.active { background: var(--border-mid); border-left: 3px solid var(--accent); }
  .blog-post-title { font-size: 13px; font-weight: 700; color: var(--text); }
  .blog-post-preview { font-size: 11px; color: var(--text-dimmer); margin-top: 4px; overflow: hidden;
                       text-overflow: ellipsis; white-space: nowrap; }
  .blog-post-meta { font-size: 10px; color: var(--text-dimmer); margin-top: 2px; }
  .blog-external-badge { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
                         background: #2ecc71; color: var(--text-bright); padding: 1px 5px; border-radius: 3px; margin-left: 6px; }
  .blog-internal-badge { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
                         background: var(--border-dark); color: var(--text-dim); padding: 1px 5px; border-radius: 3px; margin-left: 6px; }
  .blog-tag { font-size: 10px; background: var(--input-bg); color: var(--text-dim); padding: 1px 6px;
              border-radius: 4px; margin-right: 3px; display: inline-block; }
  .blog-reply { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px; padding: 12px; margin-bottom: 8px; }
  .blog-reply-author { font-size: 12px; font-weight: 700; color: var(--highlight); }
  .blog-reply-date { font-size: 10px; color: var(--text-dimmer); margin-left: 8px; }
  .blog-reply-text { font-size: 13px; color: var(--text); margin-top: 6px; line-height: 1.5; white-space: pre-wrap; }

  /* -- Events tab -- */
  #events-pane { padding: 0; flex-direction: row; }
  .events-sub-tab.active { background: var(--accent); border-color: var(--accent); color: var(--text-bright); }
  .event-card { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 10px;
                padding: 14px 16px; flex: 1 1 250px; max-width: 350px; min-width: 220px;
                transition: border-color 0.15s; }
  .event-card:hover { border-color: var(--text-dimmer); }
  .event-card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
  .event-card-name { font-size: 14px; font-weight: 700; color: var(--text); }
  .event-card-severity { font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px;
                         text-transform: uppercase; letter-spacing: 0.5px; }
  .event-sev-critical { background: #e94560; color: #fff; }
  .event-sev-high { background: #e67e22; color: #fff; }
  .event-sev-medium { background: #f39c12; color: #111; }
  .event-sev-low { background: #2ecc71; color: #111; }
  .event-card-actions { font-size: 11px; color: var(--text-dim); margin-bottom: 8px; }
  .event-card-preview { font-size: 11px; color: var(--text-dimmer); margin-bottom: 10px; overflow: hidden;
                        text-overflow: ellipsis; white-space: nowrap; }
  .event-card-btns { display: flex; gap: 4px; }
  .event-card-btns button { flex: 1; }
  .event-trigger-btn { background: var(--accent); color: var(--text-bright); border: none; padding: 5px; border-radius: 6px;
                       cursor: pointer; font-size: 11px; font-weight: 600; }
  .event-trigger-btn:hover { background: var(--accent-dark); }
  .event-log-row { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px;
                   padding: 10px 14px; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; }
  .event-log-row:hover { border-color: var(--text-dimmer); }
  .event-log-time { font-size: 11px; color: var(--text-dimmer); min-width: 80px; }
  .event-log-name { font-size: 13px; font-weight: 600; color: var(--text); flex: 1; }
  .event-log-actions { font-size: 10px; color: var(--text-dimmer); }

  /* -- Modal overlay -- */
  .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.7);
                   z-index: 1000; align-items: center; justify-content: center; }
  .modal-overlay.open { display: flex; }
  .modal { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 12px;
           padding: 24px; min-width: 380px; max-width: 500px; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
  .modal h2 { margin: 0 0 16px; font-size: 16px; color: var(--accent); }
  .modal-field { margin-bottom: 14px; }
  .modal-field label { display: block; font-size: 12px; color: var(--text-dim); margin-bottom: 4px; font-weight: 600;
                       text-transform: uppercase; letter-spacing: 0.5px; }
  .modal-field input, .modal-field select, .modal-field textarea {
    width: 100%; background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 8px 12px;
    border-radius: 8px; font-size: 14px; outline: none; box-sizing: border-box; }
  .modal-field input:focus, .modal-field select:focus, .modal-field textarea:focus { border-color: var(--accent); }
  .modal-field textarea { resize: vertical; min-height: 60px; font-family: inherit; }
  .modal-field .field-hint { font-size: 11px; color: var(--text-dimmer); margin-top: 4px; }
  .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 18px; }
  .modal-btn-primary { background: var(--accent); color: var(--text-bright); border: none; padding: 8px 20px;
                       border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 600; }
  .modal-btn-primary:hover { background: var(--accent-dark); }
  .modal-btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
  .modal-btn-cancel { background: transparent; color: var(--text-dim); border: 1px solid var(--border-dark); padding: 8px 20px;
                      border-radius: 8px; cursor: pointer; font-size: 13px; }
  .modal-btn-cancel:hover { border-color: var(--accent); color: var(--accent); }
  .modal-status { font-size: 12px; color: var(--highlight); margin-top: 10px; min-height: 16px; }

  /* -- Loading overlay -- */
  #loading-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8);
                     z-index: 2000; align-items: center; justify-content: center; flex-direction: column; gap: 12px; }
  #loading-overlay.open { display: flex; }
  #loading-overlay .spinner { width: 32px; height: 32px; border: 3px solid var(--border-dark);
                              border-top-color: var(--accent); border-radius: 50%;
                              animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  #loading-text { color: var(--text); font-size: 14px; }

  #main-layout { flex: 1; display: flex; overflow: hidden; }

  /* -- Sidebar -- */
  #sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
             display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  .sidebar-section { font-size: 11px; font-weight: 700; text-transform: uppercase;
                     letter-spacing: 1px; color: var(--text-dimmer); padding: 10px 14px 4px; }
  .channel-btn { display: flex; align-items: center; gap: 6px; width: 100%; text-align: left;
                 background: transparent; border: none; color: var(--text-dim); padding: 5px 14px;
                 font-size: 13px; cursor: pointer; transition: all 0.1s ease; }
  .channel-btn:hover { background: var(--border-mid); color: var(--text); }
  .channel-btn.active { background: var(--border-mid); color: var(--text-bright); font-weight: 700; }
  .channel-btn .unread-badge { background: var(--accent); color: var(--text-bright); font-size: 10px;
                               padding: 1px 6px; border-radius: 8px; margin-left: auto;
                               font-weight: 700; display: none; }
  .channel-btn .unread-badge.visible { display: inline; }
  .sidebar-divider { border: none; border-top: 1px solid var(--border); margin: 6px 14px; }

  /* -- Tab panes -- */
  .tab-pane { display: none; flex: 1; overflow: hidden; }
  .tab-pane.active { display: flex; }
  #chat-pane { flex-direction: row; }
  #docs-pane { flex-direction: column; }
  #chat-area { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }

  /* -- Chat tab -- */
  #channel-header { background: var(--panel); padding: 8px 20px; border-bottom: 1px solid var(--border);
                    font-size: 15px; font-weight: 700; color: var(--text); }
  #channel-header .ch-desc { font-size: 12px; color: var(--text-dim); font-weight: 400; margin-left: 10px; }
  #channel-members { font-size: 11px; color: var(--text-dimmer); margin-top: 2px; }
  #messages-panel { flex: 1; overflow-y: auto; padding: 12px 20px; display: flex;
                    flex-direction: column; gap: 6px; }
  .msg { max-width: 85%; padding: 10px 14px; border-radius: 12px; line-height: 1.5; }
  .msg-row { display: flex; gap: 10px; align-items: flex-start; }
  .msg-body { flex: 1; min-width: 0; }
  .msg-avatar { width: 32px; height: 32px; border-radius: 6px; flex-shrink: 0;
                display: flex; align-items: center; justify-content: center;
                font-size: 14px; font-weight: 700; color: #fff; margin-top: 1px; }
  .msg-avatar img { width: 32px; height: 32px; border-radius: 6px; object-fit: cover; }
  .msg .sender { font-weight: 700; font-size: 13px; margin-bottom: 4px; }
  .msg .content { font-size: 14px; word-break: break-word; }
  .msg .content h1 { font-size: 16px; margin: 8px 0 4px; color: var(--text); }
  .msg .content h2 { font-size: 15px; margin: 6px 0 3px; color: var(--text); }
  .msg .content h3 { font-size: 14px; margin: 5px 0 2px; color: var(--text); }
  .msg .content p { margin: 4px 0; }
  .msg .content ul, .msg .content ol { margin: 4px 0 4px 20px; }
  .msg .content li { margin: 2px 0; }
  .msg .content strong { color: var(--text-bright); }
  .msg .content code { background: rgba(255,255,255,0.1); padding: 1px 4px; border-radius: 3px; font-size: 13px; }
  .msg .content pre { background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; margin: 4px 0;
                      overflow-x: auto; }
  .msg .content pre code { background: none; padding: 0; }
  .msg .content hr { border: none; border-top: 1px solid var(--border-dark); margin: 8px 0; }
  .msg .content input[type="checkbox"] { margin-right: 4px; }
  .msg .ts { font-size: 11px; color: var(--text-dim); margin-top: 4px; }
  .msg-customer { align-self: flex-end; background: var(--border); border-bottom-right-radius: 4px; }
  .msg-customer .sender { color: #4fc3f7; }
  .msg-board .sender { color: #ffd700; }
  .msg-hacker .sender { color: #00ff41; }
  .msg-god .sender { color: #ff6ff2; }
  .msg-intern .sender { color: #a8e6cf; }
  .msg-competitor .sender { color: #ff4444; }
  .msg-regulator .sender { color: #ff9800; }
  .msg-investor .sender { color: #7c4dff; }
  .msg-press .sender { color: #ffab40; }
  .msg-agent { align-self: flex-start; background: var(--border-mid); border: 1px solid var(--border-dark); border-bottom-left-radius: 4px; }
  .msg-pm .sender { color: #e94560; }
  .msg-engmgr .sender { color: #f39c12; }
  .msg-architect .sender { color: #9b59b6; }
  .msg-senior .sender { color: #2ecc71; }
  .msg-support .sender { color: #1abc9c; }
  .msg-sales .sender { color: #e67e22; }
  .msg-ceo .sender { color: #f1c40f; }
  .msg-cfo .sender { color: #3498db; }
  .msg-marketing .sender { color: #e056a0; }
  .msg-devops .sender { color: #00bcd4; }
  .msg-projmgr .sender { color: #26c6da; }
  .msg-default .sender { color: #95a5a6; }

  /* -- Persona bar -- */
  #persona-bar { background: var(--sidebar); padding: 6px 20px; border-top: 1px solid var(--border);
                 display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
  /* -- Input area -- */
  #input-area { background: var(--panel); padding: 10px 20px; border-top: 1px solid var(--border);
                display: flex; gap: 8px; align-items: center; }
  #sender-name { background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                 padding: 8px 12px; border-radius: 8px; font-size: 14px; outline: none; }
  #sender-name:focus { border-color: var(--accent); }
  #sender-role, #sender-role-custom { background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                   padding: 8px 12px; border-radius: 8px; font-size: 14px; }
  #msg-input { flex: 1; background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
               padding: 10px 14px; border-radius: 8px; font-size: 14px; outline: none; }
  #msg-input:focus { border-color: var(--accent); }
  #send-btn { background: var(--accent); color: var(--text-bright); border: none; padding: 10px 20px;
              border-radius: 8px; font-size: 14px; cursor: pointer; font-weight: 600; }
  #send-btn:hover { background: var(--accent-dark); }
  #clear-btn { background: transparent; color: var(--text-dim); border: 1px solid var(--border-dark); padding: 10px 14px;
               border-radius: 8px; font-size: 14px; cursor: pointer; }
  #clear-btn:hover { border-color: var(--accent); color: var(--accent); }

  /* -- Docs tab -- */
  #docs-pane { padding: 0; flex-direction: row; }
  #docs-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                  display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  .docs-sidebar-section { font-size: 11px; font-weight: 700; text-transform: uppercase;
                          letter-spacing: 1px; color: var(--text-dimmer); padding: 10px 14px 4px; }
  .docs-sidebar-divider { border: none; border-top: 1px solid var(--border); margin: 6px 14px; }
  .folder-btn { display: flex; align-items: center; gap: 6px; width: 100%; text-align: left;
                background: transparent; border: none; color: var(--text-dim); padding: 5px 14px;
                font-size: 13px; cursor: pointer; transition: all 0.1s ease; }
  .folder-btn:hover { background: var(--border-mid); color: var(--text); }
  .folder-btn.active { background: var(--border-mid); color: var(--text-bright); font-weight: 700; }
  .folder-tree-node { padding-left: 0; }
  .folder-tree-node .folder-tree-node { padding-left: 12px; }
  .folder-tree-toggle { display: inline-flex; align-items: center; gap: 4px; width: 100%; text-align: left;
                        background: transparent; border: none; color: var(--text-dim); padding: 4px 14px;
                        font-size: 13px; cursor: pointer; }
  .folder-tree-toggle:hover { background: var(--border-mid); color: var(--text); }
  .folder-tree-toggle .arrow { display: inline-block; width: 12px; font-size: 10px; transition: transform 0.15s; }
  .folder-tree-toggle .arrow.open { transform: rotate(90deg); }
  .folder-tree-children { overflow: hidden; }
  .folder-tree-children.collapsed { display: none; }
  #new-folder-btn { background: transparent; color: var(--text-dimmer); border: 1px dashed var(--border-dark);
                    padding: 4px 14px; font-size: 12px; cursor: pointer; margin: 4px 14px; border-radius: 6px;
                    width: calc(100% - 28px); text-align: center; }
  #new-folder-btn:hover { color: var(--text); border-color: var(--text-dim); }
  #new-folder-dialog { padding: 8px 14px; display: none; flex-direction: column; gap: 6px; }
  #new-folder-dialog input { background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                             padding: 6px 10px; border-radius: 6px; font-size: 12px; outline: none; }
  #new-folder-dialog input:focus { border-color: var(--accent); }
  .new-folder-actions { display: flex; gap: 4px; }
  .new-folder-actions button { flex: 1; padding: 5px; border-radius: 6px; border: 1px solid var(--border-dark);
                               background: transparent; color: var(--text-dim); font-size: 12px; cursor: pointer; }
  .new-folder-actions button.save { background: var(--accent); color: var(--text-bright); border-color: var(--accent); }
  .folder-btn-wrap { display: flex; align-items: center; width: 100%; }
  .folder-btn-wrap .folder-btn { flex: 1; text-align: left; }
  .folder-perms-btn { background: transparent; border: none; color: var(--text-dimmer); cursor: pointer;
                      padding: 2px 6px; font-size: 13px; line-height: 1; flex-shrink: 0; opacity: 0; transition: opacity 0.15s; }
  .folder-btn-wrap:hover .folder-perms-btn { opacity: 1; }
  .folder-perms-btn:hover { color: var(--text); }
  #folder-perms-panel { display: none; padding: 10px 14px; border-top: 1px solid var(--border-dark);
                        max-height: 300px; overflow-y: auto; }
  #folder-perms-panel.open { display: block; }
  .folder-perms-title { font-size: 12px; font-weight: 700; color: var(--text-bright); margin-bottom: 6px;
                        display: flex; justify-content: space-between; align-items: center; }
  .folder-perms-title span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .folder-perms-list { display: flex; flex-direction: column; gap: 2px; margin-bottom: 8px; }
  .folder-perms-list label { font-size: 12px; color: var(--text-dim); display: flex; align-items: center; gap: 6px;
                             padding: 2px 0; cursor: pointer; }
  .folder-perms-list label:hover { color: var(--text); }
  .folder-perms-list input[type="checkbox"] { accent-color: var(--accent); }
  .folder-perms-actions { display: flex; gap: 4px; }
  .folder-perms-actions button { flex: 1; padding: 4px; border-radius: 6px; border: 1px solid var(--border-dark);
                                 background: transparent; color: var(--text-dim); font-size: 11px; cursor: pointer; }
  .folder-perms-actions button.save { background: var(--accent); color: var(--text-bright); border-color: var(--accent); }
  .folder-perms-select-all { font-size: 11px; color: var(--accent); background: none; border: none;
                             cursor: pointer; padding: 0; text-decoration: underline; }
  #docs-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
  #docs-toolbar { padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                  display: flex; align-items: center; }
  #docs-search { width: 100%; max-width: 400px; background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                 padding: 8px 12px; border-radius: 8px; font-size: 14px; outline: none; }
  #docs-search:focus { border-color: var(--accent); }
  #new-doc-btn { background: var(--accent); color: var(--text-bright); border: none; padding: 8px 16px;
                 border-radius: 8px; font-size: 13px; cursor: pointer; font-weight: 600;
                 margin-left: 8px; white-space: nowrap; }
  #new-doc-btn:hover { background: var(--accent-dark); }
  #doc-editor { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
  #doc-editor-header { display: flex; align-items: center; justify-content: space-between;
                       padding: 10px 20px; border-bottom: 1px solid var(--border); background: var(--panel); }
  #doc-editor-header button { background: transparent; color: var(--text); border: 1px solid var(--border-dark);
                              padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 13px; }
  #doc-editor-save { background: var(--accent) !important; border-color: var(--accent) !important; font-weight: 600; }
  #doc-editor-save:hover { background: var(--accent-dark) !important; }
  #doc-editor-form { flex: 1; display: flex; flex-direction: column; gap: 10px; padding: 16px 20px; overflow-y: auto; }
  #doc-editor-title { background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                      padding: 10px 14px; border-radius: 8px; font-size: 16px; font-weight: 700; outline: none; }
  #doc-editor-title:focus { border-color: var(--accent); }
  #doc-editor-folder { background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                       padding: 8px 12px; border-radius: 8px; font-size: 14px; width: 200px; }
  #doc-editor-content { flex: 1; background: var(--bg); color: var(--text); border: 1px solid var(--border-dark);
                        padding: 14px; border-radius: 8px; font-size: 14px; outline: none;
                        font-family: monospace; resize: none; min-height: 300px; }
  #doc-editor-content:focus { border-color: var(--accent); }
  #docs-list { flex: 1; overflow-y: auto; padding: 16px 20px; }
  .doc-card { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px; padding: 12px 16px;
              margin-bottom: 8px; cursor: pointer; transition: border-color 0.15s ease; }
  .doc-card:hover { border-color: var(--accent); }
  .doc-card-title { font-size: 14px; font-weight: 700; color: var(--highlight); margin-bottom: 4px; }
  .doc-card-meta { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
  .doc-card-folder { font-size: 11px; background: var(--border); color: var(--highlight); padding: 2px 8px;
                     border-radius: 4px; font-weight: 600; }
  .doc-card-preview { font-size: 13px; color: var(--text-dim); overflow: hidden; text-overflow: ellipsis;
                      white-space: nowrap; }
  #docs-empty { color: var(--text-dimmer); font-size: 14px; text-align: center; padding: 40px 20px; }
  #doc-viewer { display: none; flex-direction: column; flex: 1; overflow: hidden; }
  #doc-viewer.open { display: flex; }
  #doc-viewer-header { padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                       display: flex; align-items: center; gap: 10px; }
  #doc-back-btn { background: transparent; border: 1px solid var(--border-dark); color: var(--text-dim); padding: 6px 12px;
                  border-radius: 6px; cursor: pointer; font-size: 13px; }
  #doc-back-btn:hover { border-color: var(--accent); color: var(--accent); }
  #doc-viewer-title { font-size: 16px; font-weight: 700; color: var(--highlight); }
  #doc-viewer-content { flex: 1; overflow-y: auto; padding: 20px; font-size: 14px;
                        color: var(--text); line-height: 1.7; }
  #doc-viewer-content h1 { font-size: 20px; margin: 12px 0 8px; }
  #doc-viewer-content h2 { font-size: 17px; margin: 10px 0 6px; }
  #doc-viewer-content h3 { font-size: 15px; margin: 8px 0 4px; }
  #doc-viewer-content p { margin: 6px 0; }
  #doc-viewer-content ul, #doc-viewer-content ol { margin: 6px 0 6px 24px; }
  #doc-viewer-content li { margin: 3px 0; }
  #doc-viewer-content strong { color: var(--text-bright); }
  #doc-viewer-content code { background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 3px; }
  #doc-viewer-content pre { background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; margin: 6px 0;
                            overflow-x: auto; white-space: pre-wrap; word-break: break-word; }
  #doc-viewer-content pre code { background: none; padding: 0; }
  #doc-viewer-content hr { border: none; border-top: 1px solid var(--border-dark); margin: 10px 0; }
  #doc-viewer-content input[type="checkbox"] { margin-right: 4px; }

  /* -- GitLab tab -- */
  #gitlab-pane { padding: 0; flex-direction: row; }
  #gitlab-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                    display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  .gitlab-sidebar-section { font-size: 11px; font-weight: 700; text-transform: uppercase;
                            letter-spacing: 1px; color: var(--text-dimmer); padding: 10px 14px 4px; }
  .repo-btn { display: flex; align-items: center; gap: 6px; width: 100%; text-align: left;
              background: transparent; border: none; color: var(--text-dim); padding: 5px 14px;
              font-size: 13px; cursor: pointer; transition: all 0.1s ease; }
  .repo-btn:hover { background: var(--border-mid); color: var(--text); }
  .repo-btn.active { background: var(--border-mid); color: var(--text-bright); font-weight: 700; }
  #gitlab-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
  #gitlab-header { padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                   display: flex; align-items: center; gap: 12px; }
  #gitlab-repo-title { font-size: 16px; font-weight: 700; color: var(--highlight); }
  #gitlab-repo-desc { font-size: 13px; color: var(--text-dim); }
  .gitlab-toggle-btn { background: transparent; border: 1px solid var(--border-dark); color: var(--text-dim); padding: 6px 14px;
                       border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; }
  .gitlab-toggle-btn:hover { border-color: var(--accent); color: var(--accent); }
  .gitlab-toggle-btn.active { background: #0f3460; color: #4fc3f7; border-color: #4fc3f7; }
  #gitlab-toggle-bar { padding: 8px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                       display: flex; gap: 6px; }
  #gitlab-content { flex: 1; overflow-y: auto; padding: 16px 20px; }
  #gitlab-empty { color: var(--text-dimmer); font-size: 14px; text-align: center; padding: 40px 20px; }
  #gitlab-landing { padding: 0; }
  #gitlab-landing-filter { width: 100%; background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark);
             padding: 8px 12px; border-radius: 6px; font-size: 13px; box-sizing: border-box; margin-bottom: 12px; }
  .gl-landing-card { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px;
             border: 1px solid var(--border-dark); border-radius: 6px; margin-bottom: 6px; cursor: pointer; }
  .gl-landing-card:hover { background: var(--border-mid); border-color: var(--accent); }
  .gl-landing-name { font-size: 14px; font-weight: 600; color: var(--highlight); }
  .gl-landing-desc { font-size: 12px; color: var(--text-dim); margin-top: 2px; }
  .gl-landing-meta { font-size: 11px; color: var(--text-dimmer); white-space: nowrap; margin-left: 16px; }
  .gl-download-btn { background: transparent; border: 1px solid var(--border-dark); color: var(--text-dim); padding: 4px 10px;
             border-radius: 4px; cursor: pointer; font-size: 11px; white-space: nowrap; }
  .gl-download-btn:hover { border-color: var(--accent); color: var(--accent); }
  .gitlab-breadcrumbs { font-size: 13px; color: var(--text-dim); margin-bottom: 12px; }
  .gitlab-breadcrumbs a { color: var(--highlight); cursor: pointer; text-decoration: none; }
  .gitlab-breadcrumbs a:hover { text-decoration: underline; }
  .tree-item { display: flex; align-items: center; gap: 8px; padding: 8px 12px; border-bottom: 1px solid var(--border-dark);
               cursor: pointer; font-size: 14px; color: var(--text); }
  .tree-item:hover { background: var(--border-mid); }
  .tree-item-icon { font-size: 14px; width: 20px; text-align: center; }
  .tree-item-name { flex: 1; }
  .gitlab-file-viewer { background: var(--input-bg); border: 1px solid var(--border-dark); border-radius: 6px; padding: 16px;
                        font-family: monospace; font-size: 13px; white-space: pre-wrap; word-break: break-word;
                        color: var(--text); line-height: 1.6; }
  .commit-item { padding: 10px 12px; border-bottom: 1px solid var(--border-dark); }
  .commit-item-id { font-family: monospace; font-size: 12px; color: var(--highlight); margin-right: 8px; }
  .commit-item-msg { font-size: 14px; color: var(--text); }
  .commit-item-meta { font-size: 12px; color: var(--text-dimmer); margin-top: 4px; }

  /* -- Tickets tab -- */
  #tickets-pane { padding: 0; flex-direction: row; }
  #tickets-sidebar { width: 200px; min-width: 200px; background: var(--sidebar); border-right: 1px solid var(--border);
                     display: flex; flex-direction: column; overflow-y: auto; padding: 8px 0; }
  .tickets-sidebar-section { font-size: 11px; font-weight: 700; text-transform: uppercase;
                             letter-spacing: 1px; color: var(--text-dimmer); padding: 10px 14px 4px; }
  .tickets-filter-btn { display: flex; align-items: center; gap: 6px; width: 100%; text-align: left;
                        background: transparent; border: none; color: var(--text-dim); padding: 5px 14px;
                        font-size: 13px; cursor: pointer; transition: all 0.1s ease; }
  .tickets-filter-btn:hover { background: var(--border-mid); color: var(--text); }
  .tickets-filter-btn.active { background: var(--border-mid); color: var(--text-bright); font-weight: 700; }
  .tickets-filter-btn .tk-count { margin-left: auto; font-size: 11px; color: var(--text-dimmer); }
  #tickets-main { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
  #tickets-header { padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                    font-size: 15px; font-weight: 700; color: var(--text); }
  #tickets-list { flex: 1; overflow-y: auto; padding: 16px 20px; }
  #tickets-empty { color: var(--text-dimmer); font-size: 14px; text-align: center; padding: 40px 20px; }
  .ticket-card { background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px; padding: 12px 16px;
                 margin-bottom: 8px; cursor: pointer; transition: border-color 0.15s ease; }
  .ticket-card:hover { border-color: var(--accent); }
  .ticket-card-top { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
  .ticket-card-id { font-family: monospace; font-size: 11px; color: var(--text-dim); }
  .ticket-card-title { font-size: 14px; font-weight: 700; color: var(--text); flex: 1; }
  .ticket-card-bottom { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .tk-badge { font-size: 11px; padding: 2px 8px; border-radius: 4px; font-weight: 600; }
  .tk-status-open { background: #1b5e20; color: #a5d6a7; }
  .tk-status-in_progress { background: #0d47a1; color: #90caf9; }
  .tk-status-resolved { background: #4a148c; color: #ce93d8; }
  .tk-status-closed { background: #333; color: #888; }
  .tk-priority-low { background: #263238; color: #78909c; }
  .tk-priority-medium { background: #33691e; color: #aed581; }
  .tk-priority-high { background: #e65100; color: #ffcc80; }
  .tk-priority-critical { background: #b71c1c; color: #ef9a9a; }
  .tk-assignee { font-size: 11px; color: var(--highlight); margin-left: auto; }
  #ticket-detail { display: none; flex-direction: column; flex: 1; overflow: hidden; }
  #ticket-detail.open { display: flex; }
  #ticket-detail-header { padding: 12px 20px; border-bottom: 1px solid var(--border); background: var(--panel);
                          display: flex; align-items: center; gap: 10px; }
  #ticket-back-btn { background: transparent; border: 1px solid var(--border-dark); color: var(--text-dim); padding: 6px 12px;
                     border-radius: 6px; cursor: pointer; font-size: 13px; }
  #ticket-back-btn:hover { border-color: var(--accent); color: var(--accent); }
  #ticket-detail-title { font-size: 16px; font-weight: 700; color: var(--text); }
  #ticket-detail-id { font-family: monospace; font-size: 12px; color: var(--text-dim); margin-left: 8px; }
  #ticket-detail-content { flex: 1; overflow-y: auto; padding: 20px; font-size: 14px;
                           color: var(--text); line-height: 1.7; }
  .tk-detail-meta { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
  .tk-detail-field { font-size: 13px; color: var(--text-dim); }
  .tk-detail-field strong { color: var(--text); }
  .tk-detail-desc { background: var(--input-bg); border: 1px solid var(--border-dark); border-radius: 6px; padding: 12px;
                    margin-bottom: 16px; white-space: pre-wrap; word-break: break-word; }
  .tk-detail-deps { margin-bottom: 16px; font-size: 13px; }
  .tk-detail-deps span { color: var(--highlight); font-family: monospace; cursor: pointer; }
  .tk-comments-header { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 8px;
                        border-bottom: 1px solid var(--border-dark); padding-bottom: 4px; }
  .tk-comment { background: var(--input-bg); border-left: 3px solid var(--border); padding: 8px 12px; margin-bottom: 8px;
                border-radius: 0 6px 6px 0; }
  .tk-comment-author { font-size: 12px; font-weight: 700; color: var(--highlight); }
  .tk-comment-time { font-size: 11px; color: var(--text-dimmer); margin-left: 8px; }
  .tk-comment-text { font-size: 13px; color: var(--text); margin-top: 4px; }
  #tk-create-btn { background: var(--accent); color: var(--text-bright); border: none; padding: 6px 14px; border-radius: 6px;
                   cursor: pointer; font-size: 12px; font-weight: 600; margin-left: auto; }
  #tk-create-btn:hover { background: var(--accent-dark); }
  #tk-create-form { display: none; background: var(--bg); border: 1px solid var(--border-dark); border-radius: 8px;
                    padding: 16px; margin-bottom: 12px; }
  #tk-create-form.open { display: block; }
  .tk-form-row { display: flex; gap: 10px; margin-bottom: 10px; align-items: center; }
  .tk-form-row label { font-size: 12px; color: var(--text-dim); min-width: 70px; }
  .tk-form-input { flex: 1; background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 6px 10px;
                   border-radius: 6px; font-size: 13px; outline: none; }
  .tk-form-input:focus { border-color: var(--accent); }
  .tk-form-select { background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 6px 10px;
                    border-radius: 6px; font-size: 13px; outline: none; }
  .tk-form-textarea { flex: 1; background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 6px 10px;
                      border-radius: 6px; font-size: 13px; outline: none; resize: vertical; min-height: 60px;
                      font-family: inherit; }
  .tk-form-textarea:focus { border-color: var(--accent); }
  .tk-form-actions { display: flex; gap: 8px; justify-content: flex-end; }
  .tk-form-submit { background: var(--accent); color: var(--text-bright); border: none; padding: 6px 16px; border-radius: 6px;
                    cursor: pointer; font-size: 12px; font-weight: 600; }
  .tk-form-submit:hover { background: var(--accent-dark); }
  .tk-form-cancel { background: transparent; color: var(--text-dim); border: 1px solid var(--border-dark); padding: 6px 16px;
                    border-radius: 6px; cursor: pointer; font-size: 12px; }
  .tk-form-cancel:hover { border-color: var(--accent); color: var(--accent); }
  .tk-detail-actions { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;
                       padding-bottom: 12px; border-bottom: 1px solid var(--border-dark); }
  .tk-action-btn { background: transparent; border: 1px solid var(--border-dark); color: var(--text); padding: 5px 12px;
                   border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; }
  .tk-action-btn:hover { border-color: var(--accent); color: var(--accent); }
  .tk-action-btn.primary { background: #0d47a1; border-color: #0d47a1; color: #90caf9; }
  .tk-action-btn.primary:hover { background: #1565c0; }
  .tk-action-btn.danger { border-color: #b71c1c; color: #ef9a9a; }
  .tk-action-btn.danger:hover { background: #b71c1c; color: var(--text-bright); }
  .tk-action-btn.success { border-color: #1b5e20; color: #a5d6a7; }
  .tk-action-btn.success:hover { background: #1b5e20; color: var(--text-bright); }
  .tk-assign-row { display: flex; gap: 8px; align-items: center; }
  .tk-assign-select { background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 4px 8px;
                      border-radius: 6px; font-size: 12px; }
  .tk-comment-input-area { display: flex; gap: 8px; margin-top: 12px; align-items: flex-start; }
  .tk-comment-input { flex: 1; background: var(--input-bg); color: var(--text); border: 1px solid var(--border-dark); padding: 8px 10px;
                      border-radius: 6px; font-size: 13px; outline: none; resize: vertical; min-height: 36px;
                      font-family: inherit; }
  .tk-comment-input:focus { border-color: var(--accent); }
  .tk-comment-submit { background: var(--accent); color: var(--text-bright); border: none; padding: 8px 14px; border-radius: 6px;
                       cursor: pointer; font-size: 12px; font-weight: 600; align-self: flex-end; }
  .tk-comment-submit:hover { background: var(--accent-dark); }
</style>
</head>
<body>
<div id="header">
  <h1>CoSim</h1>
  <button class="header-tab active" data-tab="chat">Chat</button>
  <button class="header-tab" data-tab="docs">Docs</button>
  <button class="header-tab" data-tab="gitlab">GitLab</button>
  <button class="header-tab" data-tab="tickets">Tickets</button>
  <button class="header-tab" data-tab="email">Email</button>
  <button class="header-tab" data-tab="memos">Memos</button>
  <button class="header-tab" data-tab="blog">Blog</button>
  <button class="header-tab" data-tab="events">Events</button>
  <button class="header-tab" data-tab="npcs">NPCs</button>
  <button class="header-tab" data-tab="usage">Usage</button>
  <button class="header-tab" data-tab="recap">Recap</button>
  <button class="header-tab" data-tab="advanced">Advanced</button>
  <select id="theme-select" title="Theme" style="background:var(--input-bg);color:var(--text-dim);border:1px solid var(--border-dark);padding:4px 6px;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;outline:none;margin:auto 0;margin-left:8px">
    <option value="default">Default</option>
    <option value="stadium">Stadium</option>
    <option value="field">Field</option>
    <option value="solarized-dark">Solarized Dark</option>
    <option value="solarized-light">Solarized Light</option>
  </select>
  <div id="session-controls">
    <span id="orch-status" title="Orchestrator status">
      <span id="orch-dot" class="status-dot disconnected"></span>
      <span id="orch-label">Disconnected</span>
    </span>
    <button id="session-new-btn" class="session-btn" title="New session">New</button>
    <button id="session-save-btn" class="session-btn" title="Save session">Save</button>
    <select id="session-load-select" title="Load session">
      <option value="" disabled selected>Load...</option>
    </select>
  </div>
</div>
<div id="main-layout">
  <!-- Chat tab: sidebar + chat area -->
  <div id="chat-pane" class="tab-pane active">
    <div id="sidebar">
      <div class="sidebar-section">Internal</div>
      <div id="internal-channels"></div>
      <hr class="sidebar-divider">
      <div class="sidebar-section">External</div>
      <div id="external-channels"></div>
      <hr class="sidebar-divider">
      <div class="sidebar-section">Scenario Director</div>
      <div id="director-channels"></div>
      <hr class="sidebar-divider">
      <div class="sidebar-section">System</div>
      <div id="system-channels"></div>
    </div>
    <div id="chat-area">
      <div id="channel-header">
        <span id="channel-title">#general</span>
        <span class="ch-desc" id="channel-desc"></span>
        <div id="channel-members"></div>
      </div>
      <div id="messages-panel"></div>
      <div id="persona-bar">
        <input id="sender-name" type="text" placeholder="Your name..." value="" style="width:120px" />
        <select id="sender-role"></select>
        <input id="sender-role-custom" type="text" placeholder="Custom role..." style="width:100px;display:none" />
      </div>
      <div id="input-area">
        <input id="msg-input" type="text" placeholder="Type a message..." autocomplete="off" />
        <button id="send-btn">Send</button>
      </div>
    </div>
  </div>
  <!-- Docs tab -->
  <div id="docs-pane" class="tab-pane">
    <div id="docs-sidebar">
      <div class="docs-sidebar-section">All</div>
      <button class="folder-btn active" data-folder="" id="folder-all">All Folders</button>
      <hr class="docs-sidebar-divider">
      <div id="folder-tree-container"></div>
      <hr class="docs-sidebar-divider">
      <button id="new-folder-btn">+ New Folder</button>
      <div id="new-folder-dialog">
        <input id="new-folder-name" type="text" placeholder="folder name (e.g. projects/my-project)" />
        <input id="new-folder-desc" type="text" placeholder="description (optional)" />
        <div style="display:flex;align-items:center;gap:6px">
          <label style="font-size:11px;color:var(--text-dim);cursor:pointer;display:flex;align-items:center;gap:4px">
            <input type="checkbox" id="new-folder-all-access" checked> Grant all agents access
          </label>
        </div>
        <div id="new-folder-access-list" class="folder-perms-list" style="display:none;max-height:150px;overflow-y:auto"></div>
        <div class="new-folder-actions">
          <button id="new-folder-cancel">Cancel</button>
          <button id="new-folder-save" class="save">Create</button>
        </div>
      </div>
      <div id="folder-perms-panel">
        <div class="folder-perms-title">
          <span id="folder-perms-name"></span>
          <button class="folder-perms-select-all" id="folder-perms-toggle-all">all</button>
        </div>
        <div class="folder-perms-list" id="folder-perms-list"></div>
        <div class="folder-perms-actions">
          <button id="folder-perms-cancel">Cancel</button>
          <button id="folder-perms-save" class="save">Save</button>
        </div>
      </div>
    </div>
    <div id="docs-main">
      <div id="docs-toolbar">
        <input id="docs-search" type="text" placeholder="Search documents..." autocomplete="off" />
        <button id="new-doc-btn">+ New Document</button>
      </div>
      <div id="doc-editor" style="display:none">
        <div id="doc-editor-header">
          <button id="doc-editor-cancel">Cancel</button>
          <span style="font-weight:700;font-size:14px">New Document</span>
          <button id="doc-editor-save">Save</button>
        </div>
        <div id="doc-editor-form">
          <input id="doc-editor-title" type="text" placeholder="Document title..." autocomplete="off" />
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
            <select id="doc-editor-folder">
            </select>
            <span style="font-size:11px;color:var(--text-dimmer)">Author:</span>
            <input id="doc-author-name" type="text" placeholder="Your name..." style="width:120px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px" />
            <select id="doc-author-role" style="background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px"></select>
          </div>
          <textarea id="doc-editor-content" placeholder="Write your document content here (Markdown supported)..." rows="16"></textarea>
        </div>
      </div>
      <div id="docs-list">
        <div id="docs-empty">No documents yet.</div>
      </div>
      <div id="doc-viewer">
        <div id="doc-viewer-header">
          <button id="doc-back-btn">Back</button>
          <span id="doc-viewer-title"></span>
          <div style="margin-left:auto;display:flex;gap:6px">
            <button id="doc-download-btn" class="session-btn" style="font-size:11px">Download</button>
            <button id="doc-history-btn" class="session-btn" style="font-size:11px">History</button>
            <button id="doc-edit-btn" class="session-btn" style="font-size:11px">Edit Latest Version</button>
          </div>
        </div>
        <div id="doc-viewer-body" style="display:flex;flex:1;min-height:0;overflow:hidden">
          <div id="doc-viewer-content" style="flex:1;overflow-y:auto"></div>
          <div id="doc-history-panel" style="display:none;width:220px;min-width:220px;border-left:1px solid var(--border-dark);background:var(--sidebar);overflow-y:auto">
            <div style="padding:8px 12px;font-size:11px;font-weight:700;color:var(--text-dimmer);text-transform:uppercase;letter-spacing:0.5px">Version History</div>
            <div id="doc-history-list"></div>
          </div>
        </div>
        <div id="doc-edit-area" style="display:none;flex:1;min-height:0;flex-direction:column;padding:12px 20px;gap:8px">
          <div style="display:flex;gap:8px;align-items:center">
            <span style="font-size:11px;color:var(--text-dimmer)">Editing as:</span>
            <input id="doc-edit-author-name" type="text" placeholder="Your name..." style="width:120px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px" />
            <select id="doc-edit-author-role" style="background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px"></select>
            <div style="margin-left:auto;display:flex;gap:6px">
              <button id="doc-edit-cancel" class="session-btn" style="font-size:11px">Cancel</button>
              <button id="doc-edit-save" class="session-btn" style="font-size:11px;background:var(--accent);border-color:var(--accent);color:var(--text-bright)">Save</button>
            </div>
          </div>
          <textarea id="doc-edit-textarea" style="flex:1;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:14px;border-radius:8px;font-size:14px;font-family:monospace;resize:none;outline:none"></textarea>
        </div>
      </div>
    </div>
  </div>
  <!-- GitLab tab -->
  <div id="gitlab-pane" class="tab-pane">
    <div id="gitlab-sidebar">
      <div class="gitlab-sidebar-section" style="cursor:pointer" onclick="glCurrentRepo=null;glCurrentPath='';renderRepoSidebar();renderRepoLanding()">Repositories</div>
      <div id="gitlab-repo-list"></div>
      <div style="padding:8px 10px">
        <button id="gl-new-repo-btn" class="session-btn" style="width:100%;font-size:11px">+ New Repo</button>
      </div>
      <div id="gl-new-repo-form" style="display:none;padding:4px 10px 10px">
        <input id="gl-new-repo-name" type="text" placeholder="repo-name" autocomplete="off"
               style="width:100%;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px;margin-bottom:6px;box-sizing:border-box" />
        <input id="gl-new-repo-desc" type="text" placeholder="Description (optional)" autocomplete="off"
               style="width:100%;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:5px 8px;border-radius:6px;font-size:12px;margin-bottom:6px;box-sizing:border-box" />
        <div style="display:flex;gap:4px">
          <button id="gl-new-repo-cancel" class="session-btn" style="flex:1;font-size:11px">Cancel</button>
          <button id="gl-new-repo-save" class="session-btn" style="flex:1;font-size:11px;background:var(--accent);border-color:var(--accent);color:var(--text-bright)">Create</button>
        </div>
      </div>
    </div>
    <div id="gitlab-main">
      <div id="gitlab-header" style="display:flex;align-items:center;justify-content:space-between">
        <div>
          <span id="gitlab-repo-title">Select a repository</span>
          <span id="gitlab-repo-desc"></span>
        </div>
        <button id="gl-repo-download-btn" class="gl-download-btn" style="display:none" onclick="glDownloadRepo(glCurrentRepo)">Download .tar.gz</button>
      </div>
      <div id="gitlab-toggle-bar">
        <button class="gitlab-toggle-btn active" data-view="tree" id="gl-toggle-tree">Files</button>
        <button class="gitlab-toggle-btn" data-view="commits" id="gl-toggle-commits">Commits</button>
      </div>
      <div id="gitlab-content">
        <div id="gitlab-empty">No repositories yet.</div>
      </div>
    </div>
  </div>
  <!-- Tickets tab -->
  <div id="tickets-pane" class="tab-pane">
    <div id="tickets-sidebar">
      <div class="tickets-sidebar-section">Status Filter</div>
      <button class="tickets-filter-btn active" data-status="" id="tk-filter-all">All <span class="tk-count" id="tk-count-all"></span></button>
      <button class="tickets-filter-btn" data-status="open">Open <span class="tk-count" id="tk-count-open"></span></button>
      <button class="tickets-filter-btn" data-status="in_progress">In Progress <span class="tk-count" id="tk-count-in_progress"></span></button>
      <button class="tickets-filter-btn" data-status="resolved">Resolved <span class="tk-count" id="tk-count-resolved"></span></button>
      <button class="tickets-filter-btn" data-status="closed">Closed <span class="tk-count" id="tk-count-closed"></span></button>
    </div>
    <div id="tickets-main">
      <div id="tickets-header" style="display:flex;align-items:center;">
        <span>Tickets</span>
        <button id="tk-create-btn" onclick="toggleCreateForm()">+ New Ticket</button>
      </div>
      <div id="tickets-list">
        <div id="tk-create-form">
          <div class="tk-form-row">
            <label>Title</label>
            <input class="tk-form-input" id="tk-form-title" placeholder="Ticket title" />
          </div>
          <div class="tk-form-row">
            <label>Priority</label>
            <select class="tk-form-select" id="tk-form-priority">
              <option value="low">Low</option>
              <option value="medium" selected>Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
            <label style="margin-left:12px;">Assignee</label>
            <select class="tk-form-select" id="tk-form-assignee">
              <option value="">Unassigned</option>
            </select>
          </div>
          <div class="tk-form-row">
            <label>Created by</label>
            <select class="tk-form-select" id="tk-form-author">
            </select>
          </div>
          <div class="tk-form-row">
            <label>Description</label>
            <textarea class="tk-form-textarea" id="tk-form-desc" placeholder="Describe the work to be done..."></textarea>
          </div>
          <div class="tk-form-row">
            <label>Notify channel</label>
            <select class="tk-form-select" id="tk-form-notify">
              <option value="">Don't notify</option>
            </select>
          </div>
          <div class="tk-form-actions">
            <button class="tk-form-cancel" onclick="toggleCreateForm()">Cancel</button>
            <button class="tk-form-submit" onclick="submitCreateTicket()">Create Ticket</button>
          </div>
        </div>
        <div id="tickets-empty">No tickets yet.</div>
      </div>
      <div id="ticket-detail">
        <div id="ticket-detail-header">
          <button id="ticket-back-btn">Back</button>
          <span id="ticket-detail-title"></span>
          <span id="ticket-detail-id"></span>
        </div>
        <div style="padding:8px 20px;background:var(--sidebar);border-bottom:1px solid var(--border-dark);display:flex;align-items:center;gap:8px">
          <span style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px">Acting as</span>
          <select class="tk-form-select" id="tk-acting-as" style="font-size:12px;">
          </select>
          <span style="font-size:10px;color:var(--text-dimmer)">All actions (status, assign, comments) use this identity</span>
        </div>
        <div id="ticket-detail-content"></div>
      </div>
    </div>
  </div>
  <!-- NPCs tab -->
  <div id="npcs-pane" class="tab-pane">
    <div id="npcs-sidebar">
      <div class="sidebar-section">Scenario</div>
      <div id="npcs-scenario-info" style="padding:8px 14px;font-size:12px;color:var(--text-dim);">No scenario loaded</div>
      <hr class="sidebar-divider">
      <div class="sidebar-section">Summary</div>
      <div id="npcs-summary" style="padding:8px 14px;font-size:12px;color:var(--text-dim);"></div>
      <hr class="sidebar-divider">
      <div style="padding:8px 10px">
        <button id="npc-hire-btn" class="session-btn" style="width:100%;background:#2ecc71;border-color:#2ecc71;color:var(--text-bright);font-size:11px">+ Hire Agent</button>
      </div>
    </div>
    <div id="npcs-main">
      <div id="npcs-content">
        <div id="npcs-empty">No scenario loaded. Click New to start a session.</div>
      </div>
    </div>
  </div>
  <!-- Events tab -->
  <div id="events-pane" class="tab-pane">
    <div style="flex:1;display:flex;flex-direction:column;overflow:hidden">
      <div style="padding:10px 20px;background:var(--panel);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px">
        <button class="session-btn events-sub-tab active" data-events-tab="pool">Event Pool</button>
        <button class="session-btn events-sub-tab" data-events-tab="log">Event Log</button>
        <div style="margin-left:auto">
          <button id="events-add-btn" class="session-btn" style="background:#2ecc71;border-color:#2ecc71;color:var(--text-bright);font-size:11px">+ Add Event</button>
        </div>
      </div>
      <div id="events-pool-view" style="flex:1;overflow-y:auto;padding:20px">
        <div id="events-pool-grid" style="display:flex;flex-wrap:wrap;gap:12px"></div>
        <div id="events-pool-empty" style="color:var(--text-dimmer);text-align:center;padding:40px">No events configured for this scenario.</div>
      </div>
      <div id="events-log-view" style="flex:1;overflow-y:auto;padding:20px;display:none">
        <div id="events-log-list"></div>
        <div id="events-log-empty" style="color:var(--text-dimmer);text-align:center;padding:40px">No events fired yet.</div>
      </div>
    </div>
  </div>
  <!-- Usage tab -->
  <div id="usage-pane" class="tab-pane">
    <div id="usage-sidebar">
      <div class="usage-sidebar-section">Session Totals</div>
      <div id="usage-totals" style="padding:4px 0;"></div>
    </div>
    <div id="usage-main">
      <div id="usage-content">
        <div id="usage-empty">No usage data yet. Send messages so agents produce responses.</div>
      </div>
    </div>
  </div>
  <!-- Recap tab -->
  <div id="recap-pane" class="tab-pane">
    <div id="recap-sidebar">
      <div class="sidebar-section">Generate Recap</div>
      <div style="padding:8px 14px">
        <select id="recap-style" style="width:100%;background:var(--bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:6px;font-size:12px;margin-bottom:8px">
          <option value="normal">Normal</option>
          <option value="ye-olde-english">Ye Olde English</option>
          <option value="tolkien">Tolkien Fantasy</option>
          <option value="star-wars">Star Wars Crawl</option>
          <option value="star-trek">Star Trek Captain's Log</option>
          <option value="dr-who">Doctor Who</option>
          <option value="morse-code">Morse Code / Telegraph</option>
          <option value="dr-seuss">Dr. Seuss</option>
          <option value="shakespeare">Shakespearean</option>
          <option value="80s-rock-ballad">80s Rock Ballad</option>
          <option value="90s-alternative">90s Alternative</option>
          <option value="heavy-metal">Heavy Metal</option>
          <option value="dystopian">Dystopian</option>
          <option value="matrix">The Matrix</option>
          <option value="pharaoh">Pharaoh's Decree</option>
          <option value="tombstone">Tombstone Western</option>
          <option value="survivor">Survivor Tribal Council</option>
          <option value="hackernews">HackerNews Blog Post</option>
        </select>
        <button id="recap-generate-btn" class="session-btn" style="width:100%;background:var(--accent);border-color:var(--accent);color:var(--text-bright);font-size:12px">Generate Recap</button>
      </div>
      <hr class="sidebar-divider">
      <div class="sidebar-section">Saved Recaps</div>
      <div id="recap-list" style="flex:1;overflow-y:auto"></div>
    </div>
    <div id="recap-main">
      <div id="recap-content" style="padding:20px;font-size:14px;color:var(--text);line-height:1.8;white-space:pre-wrap">
        <div id="recap-empty" style="color:var(--text-dimmer);text-align:center;padding:60px">Pick a style and generate a recap of this session.</div>
      </div>
    </div>
  </div>
  <!-- Email tab -->
  <div id="email-pane" class="tab-pane">
    <div id="email-sidebar">
      <div style="padding:10px;border-bottom:1px solid var(--border-dark)">
        <button id="compose-email-btn" class="session-btn" style="width:100%;background:#3498db;border-color:#3498db;color:var(--text-bright);font-size:12px">Compose Email</button>
      </div>
      <div id="email-list" style="flex:1;overflow-y:auto"></div>
      <div id="email-list-empty" style="color:var(--text-dimmer);text-align:center;padding:20px;font-size:12px">No emails sent yet.</div>
    </div>
    <div id="email-main">
      <div id="email-viewer" style="display:none">
        <div id="email-viewer-from" style="font-size:13px;color:var(--highlight);font-weight:700;margin-bottom:4px"></div>
        <div id="email-viewer-subject" style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:4px"></div>
        <div id="email-viewer-date" style="font-size:11px;color:var(--text-dimmer);margin-bottom:16px"></div>
        <div id="email-viewer-body" style="font-size:14px;color:var(--text);line-height:1.6;white-space:pre-wrap"></div>
      </div>
      <div id="email-compose" style="display:none;max-width:600px">
        <h3 style="color:var(--text);margin-bottom:12px">Compose Email</h3>
        <div class="modal-field">
          <label>From</label>
          <div style="display:flex;gap:8px">
            <input id="email-compose-name" type="text" placeholder="Name" style="flex:1" autocomplete="off" />
            <select id="email-compose-role" style="flex:1"></select>
          </div>
          <input id="email-compose-role-custom" type="text" placeholder="Custom role..." style="display:none;width:100%;margin-top:6px" autocomplete="off" />
        </div>
        <div class="modal-field">
          <label>Subject</label>
          <input id="email-compose-subject" type="text" placeholder="Subject line..." autocomplete="off" />
        </div>
        <div class="modal-field">
          <label>Body</label>
          <textarea id="email-compose-body" style="width:100%;min-height:200px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:14px;border-radius:8px;font-size:14px;font-family:inherit;resize:vertical;line-height:1.6" placeholder="Write your email..."></textarea>
        </div>
        <div style="display:flex;gap:8px;justify-content:flex-end">
          <button class="session-btn" id="email-compose-cancel">Cancel</button>
          <button class="modal-btn-primary" id="email-compose-send" style="background:#3498db">Send</button>
        </div>
      </div>
      <div id="email-empty-state" style="color:var(--text-dimmer);text-align:center;padding:60px;font-size:14px">Select an email to read, or compose a new one.</div>
    </div>
  </div>
  <!-- Memos tab -->
  <div id="memos-pane" class="tab-pane">
    <div id="memos-sidebar">
      <div style="padding:10px;border-bottom:1px solid var(--border-dark)">
        <button id="create-memo-thread-btn" class="session-btn" style="width:100%;background:#2ecc71;border-color:#2ecc71;color:var(--text-bright);font-size:12px">New Discussion</button>
      </div>
      <div id="memo-threads-list" style="flex:1;overflow-y:auto"></div>
      <div id="memo-threads-empty" style="color:var(--text-dimmer);text-align:center;padding:20px;font-size:12px">No discussion threads yet.</div>
    </div>
    <div id="memos-main">
      <div id="memo-thread-viewer" style="display:none">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px">
          <div>
            <h2 id="memo-thread-title" style="color:var(--text);margin:0 0 4px 0;font-size:18px"></h2>
            <div id="memo-thread-meta" style="font-size:11px;color:var(--text-dimmer)"></div>
            <div id="memo-thread-description" style="font-size:13px;color:var(--text-dim);margin-top:8px"></div>
          </div>
          <button id="memo-delete-btn" style="background:transparent;border:1px solid var(--accent);color:var(--accent);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer" title="Delete thread">Delete</button>
        </div>
        <div id="memo-posts-list" style="margin:16px 0"></div>
        <div style="border-top:1px solid var(--border-dark);padding-top:12px">
          <div style="display:flex;gap:8px;margin-bottom:8px">
            <input id="memo-reply-name" type="text" placeholder="Name" style="flex:1;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px" autocomplete="off" />
            <select id="memo-reply-role" style="flex:1;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px"></select>
          </div>
          <input id="memo-reply-role-custom" type="text" placeholder="Custom role..." style="display:none;width:100%;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px;margin-bottom:8px;box-sizing:border-box" autocomplete="off" />
          <textarea id="memo-reply-text" placeholder="Post a reply..." style="width:100%;min-height:80px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:10px;border-radius:6px;font-family:inherit;resize:vertical;font-size:13px;box-sizing:border-box"></textarea>
          <div style="display:flex;gap:8px;margin-top:8px;justify-content:flex-end">
            <button id="memo-reply-send" class="modal-btn-primary" style="background:#2ecc71;font-size:12px">Post Reply</button>
          </div>
        </div>
      </div>
      <div id="memo-empty-state" style="color:var(--text-dimmer);text-align:center;padding:60px;font-size:14px">Select a discussion thread or create a new one.</div>
    </div>
  </div>
  <!-- Blog tab -->
  <div id="blog-pane" class="tab-pane">
    <div id="blog-sidebar">
      <div style="padding:10px;border-bottom:1px solid var(--border-dark)">
        <button id="create-blog-post-btn" class="session-btn" style="width:100%;background:var(--accent);border-color:var(--accent);color:var(--text-bright);font-size:12px">New Post</button>
      </div>
      <div class="blog-filter-bar">
        <button class="blog-filter-btn active" data-blog-filter="all">All</button>
        <button class="blog-filter-btn" data-blog-filter="internal">Internal</button>
        <button class="blog-filter-btn" data-blog-filter="external">External</button>
      </div>
      <div id="blog-posts-list" style="flex:1;overflow-y:auto"></div>
      <div id="blog-posts-empty" style="color:var(--text-dimmer);text-align:center;padding:20px;font-size:12px">No blog posts yet.</div>
    </div>
    <div id="blog-main">
      <div id="blog-post-viewer" style="display:none">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px">
          <div>
            <div style="display:flex;align-items:center">
              <h2 id="blog-post-title" style="color:var(--text);margin:0;font-size:20px"></h2>
              <span id="blog-post-badge"></span>
            </div>
            <div id="blog-post-author" style="font-size:13px;color:var(--highlight);font-weight:700;margin-top:4px"></div>
            <div id="blog-post-date" style="font-size:11px;color:var(--text-dimmer);margin-top:2px"></div>
            <div id="blog-post-tags" style="margin-top:6px"></div>
          </div>
          <div style="display:flex;gap:4px">
            <button id="blog-publish-btn" style="background:#2ecc71;border:none;color:var(--text-bright);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer;display:none" title="Publish">Publish</button>
            <button id="blog-unpublish-btn" style="background:transparent;border:1px solid #f39c12;color:#f39c12;padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer;display:none" title="Unpublish">Unpublish</button>
            <button id="blog-download-btn" style="background:transparent;border:1px solid var(--text-dim);color:var(--text-dim);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer" title="Download raw content">Download</button>
            <button id="blog-delete-btn" style="background:transparent;border:1px solid var(--accent);color:var(--accent);padding:4px 10px;border-radius:4px;font-size:11px;cursor:pointer" title="Delete post">Delete</button>
          </div>
        </div>
        <div id="blog-post-body" style="font-size:14px;color:var(--text);line-height:1.7;margin-bottom:20px"></div>
        <div style="border-top:1px solid var(--border-dark);padding-top:12px">
          <h3 id="blog-replies-header" style="font-size:14px;color:var(--text);margin-bottom:10px"></h3>
          <div id="blog-replies-list" style="margin-bottom:16px"></div>
          <div style="display:flex;gap:8px;margin-bottom:8px">
            <input id="blog-reply-name" type="text" placeholder="Name" style="flex:1;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px" autocomplete="off" />
            <select id="blog-reply-role" style="flex:1;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px"></select>
          </div>
          <input id="blog-reply-role-custom" type="text" placeholder="Custom role..." style="display:none;width:100%;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:4px;font-size:12px;margin-bottom:8px;box-sizing:border-box" autocomplete="off" />
          <textarea id="blog-reply-text" placeholder="Write a reply..." style="width:100%;min-height:60px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:10px;border-radius:6px;font-family:inherit;resize:vertical;font-size:13px;box-sizing:border-box"></textarea>
          <div style="display:flex;gap:8px;margin-top:8px;justify-content:flex-end">
            <button id="blog-reply-send" class="modal-btn-primary" style="font-size:12px">Post Reply</button>
          </div>
        </div>
      </div>
      <div id="blog-empty-state" style="color:var(--text-dimmer);text-align:center;padding:60px;font-size:14px">No blog posts yet — write the first one.</div>
    </div>
  </div>
  <!-- Advanced tab -->
  <div id="advanced-pane" class="tab-pane">
    <div id="advanced-main" style="flex:1;padding:20px;overflow-y:auto">
      <div style="max-width:800px">
        <h3 style="color:var(--text);margin-bottom:16px">Advanced Actions</h3>

        <!-- Session Manager -->
        <div style="margin-bottom:32px">
          <div style="font-size:12px;font-weight:600;color:var(--text);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Session Manager</div>
          <p style="font-size:12px;color:var(--text-dim);margin-bottom:12px">Manage saved sessions — load, rename, or delete.</p>
          <div id="session-manager-table-wrap" style="overflow-x:auto">
            <table id="session-manager-table" style="width:100%;border-collapse:collapse;font-size:13px">
              <thead>
                <tr style="border-bottom:1px solid var(--border-dark);text-align:left">
                  <th data-sm-sort="name" style="padding:8px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Name <span class="sm-sort-arrow"></span></th>
                  <th data-sm-sort="scenario" style="padding:8px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Scenario <span class="sm-sort-arrow"></span></th>
                  <th data-sm-sort="created_at" style="padding:8px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Created <span class="sm-sort-arrow"></span></th>
                  <th data-sm-sort="saved_at" style="padding:8px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Last Saved <span class="sm-sort-arrow"></span></th>
                  <th style="padding:8px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;text-align:right">Actions</th>
                </tr>
              </thead>
              <tbody id="session-manager-body">
                <tr><td colspan="5" style="padding:16px 10px;color:var(--text-dim);text-align:center">Loading...</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- The Loaf — Notification History -->
        <div style="margin-bottom:32px">
          <div style="font-size:12px;font-weight:600;color:var(--text);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">The Loaf, Starchy Version <span style="font-size:10px;color:var(--text-dimmer);text-transform:none;letter-spacing:0">Notification History</span></div>
          <p style="font-size:12px;color:var(--text-dim);margin-bottom:12px">All toast notifications from this session. Useful for reviewing messages that disappeared too quickly.</p>
          <div style="display:flex;gap:8px;margin-bottom:10px">
            <button id="loaf-refresh-btn" class="session-btn" style="font-size:11px">Refresh</button>
            <button id="loaf-clear-btn" class="session-btn" style="font-size:11px;border-color:var(--accent);color:var(--accent)">Clear Log</button>
            <span id="loaf-count" style="font-size:11px;color:var(--text-dimmer);align-self:center;margin-left:auto"></span>
          </div>
          <div id="loaf-table-wrap" style="overflow-x:auto;max-height:300px;overflow-y:auto;border:1px solid var(--border-dark);border-radius:6px">
            <table style="width:100%;border-collapse:collapse;font-size:12px">
              <thead>
                <tr style="border-bottom:1px solid var(--border-dark);position:sticky;top:0;background:var(--panel)">
                  <th style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:10px;text-transform:uppercase;text-align:left;width:80px">Time</th>
                  <th style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:10px;text-transform:uppercase;text-align:left">Message</th>
                </tr>
              </thead>
              <tbody id="loaf-body">
                <tr><td colspan="2" style="padding:12px 10px;color:var(--text-dimmer);text-align:center">No notifications yet</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Danger Zone -->
        <div style="margin-bottom:24px">
          <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Danger Zone</div>
          <p style="font-size:12px;color:var(--text-dim);margin-bottom:12px">These actions are destructive and cannot be undone. Save your session first.</p>
          <button id="clear-chat-btn" class="session-btn" style="border-color:var(--accent);color:var(--accent);margin-right:8px">Clear Chat History</button>
          <button id="clear-all-btn" class="session-btn" style="background:var(--accent);border-color:var(--accent);color:var(--text-bright)">Clear Everything</button>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Blog Create Post Modal -->
<div class="modal-overlay" id="blog-create-modal">
  <div class="modal" style="max-width:600px">
    <h2>New Blog Post</h2>
    <div class="modal-field">
      <label>Author</label>
      <div style="display:flex;gap:8px">
        <input id="blog-create-name" type="text" placeholder="Name" style="flex:1" autocomplete="off" />
        <select id="blog-create-role" style="flex:1"></select>
      </div>
      <input id="blog-create-role-custom" type="text" placeholder="Custom role..." style="display:none;width:100%;margin-top:6px" autocomplete="off" />
    </div>
    <div class="modal-field">
      <label>Title</label>
      <input id="blog-create-title" type="text" placeholder="Blog post title..." autocomplete="off" />
    </div>
    <div class="modal-field">
      <label>Body</label>
      <textarea id="blog-create-body" style="width:100%;min-height:200px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:14px;border-radius:8px;font-size:14px;font-family:inherit;resize:vertical;line-height:1.6;box-sizing:border-box" placeholder="Write your blog post..."></textarea>
    </div>
    <div class="modal-field">
      <label>Tags (comma-separated)</label>
      <input id="blog-create-tags" type="text" placeholder="engineering, api, release" autocomplete="off" />
    </div>
    <div class="modal-field" style="display:flex;align-items:center;gap:8px">
      <input id="blog-create-external" type="checkbox" style="accent-color:var(--accent)" />
      <label style="margin:0;text-transform:none;letter-spacing:0;font-size:13px;color:var(--text)">External (customer-facing)</label>
    </div>
    <div class="modal-actions">
      <button class="session-btn" id="blog-create-cancel">Cancel</button>
      <button class="session-btn" id="blog-create-draft" style="border-color:#f39c12;color:#f39c12">Save Draft</button>
      <button class="modal-btn-primary" id="blog-create-submit">Publish</button>
    </div>
  </div>
</div>

<!-- Memo Create Thread Modal -->
<div class="modal-overlay" id="memo-create-modal">
  <div class="modal" style="max-width:500px">
    <h2>New Discussion Thread</h2>
    <div class="modal-field">
      <label>Posted by</label>
      <div style="display:flex;gap:8px">
        <input id="memo-create-name" type="text" placeholder="Name" style="flex:1" autocomplete="off" />
        <select id="memo-create-role" style="flex:1"></select>
      </div>
      <input id="memo-create-role-custom" type="text" placeholder="Custom role..." style="display:none;width:100%;margin-top:6px" autocomplete="off" />
    </div>
    <div class="modal-field">
      <label>Title</label>
      <input id="memo-create-title" type="text" placeholder="Discussion thread title..." autocomplete="off" />
    </div>
    <div class="modal-field">
      <label>Description (optional)</label>
      <textarea id="memo-create-description" style="width:100%;min-height:60px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:10px;border-radius:6px;font-family:inherit;resize:vertical;font-size:13px;box-sizing:border-box" placeholder="Brief description of the discussion topic..."></textarea>
    </div>
    <div class="modal-actions">
      <button class="session-btn" id="memo-create-cancel">Cancel</button>
      <button class="modal-btn-primary" id="memo-create-submit" style="background:#2ecc71">Create Thread</button>
    </div>
  </div>
</div>

<!-- New Session Modal -->
<div class="modal-overlay" id="new-session-modal">
  <div class="modal">
    <h2>New Session</h2>
    <div class="modal-field">
      <label>Scenario</label>
      <select id="new-session-scenario"></select>
      <div class="field-hint" id="new-session-scenario-desc"></div>
    </div>
    <div class="modal-field">
      <label>Session Name (optional)</label>
      <input id="new-session-name" type="text" placeholder="e.g. consulting-run" autocomplete="off" />
      <div class="field-hint">Leave blank to auto-generate from scenario + date</div>
    </div>
    <div class="modal-status" id="new-session-status"></div>
    <div class="modal-actions">
      <button class="modal-btn-cancel" id="new-session-cancel">Cancel</button>
      <button class="modal-btn-primary" id="new-session-confirm">Create</button>
    </div>
  </div>
</div>

<!-- Save Session Modal -->
<div class="modal-overlay" id="save-session-modal">
  <div class="modal" style="max-width:480px">
    <h2>Save Session</h2>
    <div class="modal-field" id="save-session-existing-wrap">
      <label>Existing saves</label>
      <div id="save-session-list" style="max-height:180px;overflow-y:auto;border:1px solid var(--border-dark);border-radius:6px;background:var(--bg-darker,var(--bg))">
        <div style="padding:12px;color:var(--text-dim);text-align:center;font-size:12px">Loading...</div>
      </div>
    </div>
    <div class="modal-field">
      <label>Save as</label>
      <input id="save-session-name" type="text" placeholder="e.g. before-demo" autocomplete="off" />
      <div class="field-hint">Leave blank to auto-generate. Click an existing save to branch from it.</div>
    </div>
    <div class="modal-status" id="save-session-status"></div>
    <div class="modal-actions">
      <button class="modal-btn-cancel" id="save-session-cancel">Cancel</button>
      <button class="modal-btn-primary" id="save-session-confirm">Save</button>
    </div>
  </div>
</div>

<!-- Load Session Modal -->
<div class="modal-overlay" id="load-session-modal">
  <div class="modal" style="max-width:600px">
    <h2>Load Session</h2>
    <div class="modal-field">
      <label>Saved Sessions</label>
      <div style="max-height:280px;overflow-y:auto;border:1px solid var(--border-dark);border-radius:6px">
        <table id="load-session-table" style="width:100%;border-collapse:collapse;font-size:13px">
          <thead>
            <tr style="border-bottom:1px solid var(--border-dark);text-align:left;position:sticky;top:0;background:var(--bg-surface,var(--bg))">
              <th data-lm-sort="name" style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Name <span class="lm-sort-arrow"></span></th>
              <th data-lm-sort="scenario" style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Scenario <span class="lm-sort-arrow"></span></th>
              <th data-lm-sort="created_at" style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Created <span class="lm-sort-arrow"></span></th>
              <th data-lm-sort="saved_at" style="padding:6px 10px;color:var(--text-dim);font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;cursor:pointer;user-select:none">Last Saved <span class="lm-sort-arrow"></span></th>
            </tr>
          </thead>
          <tbody id="load-session-body">
            <tr><td colspan="4" style="padding:16px 10px;color:var(--text-dim);text-align:center">Loading...</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="modal-status" id="load-session-status"></div>
    <div class="modal-actions">
      <button class="modal-btn-cancel" id="load-session-cancel">Cancel</button>
      <button class="modal-btn-primary" id="load-session-confirm" disabled>Load</button>
    </div>
  </div>
</div>

<!-- NPC Detail Modal -->
<div class="modal-overlay" id="npc-detail-modal">
  <div class="modal" style="width:80vw;max-width:1000px;height:75vh;display:flex;flex-direction:column">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
      <h2 id="npc-detail-title" style="margin:0"></h2>
      <button class="modal-btn-cancel" id="npc-detail-close">Close</button>
    </div>
    <div style="display:flex;gap:8px;margin-bottom:12px">
      <button class="session-btn npc-detail-tab active" data-npc-tab="thoughts">Thoughts</button>
      <button class="session-btn npc-detail-tab" data-npc-tab="character">Character</button>
      <button class="session-btn npc-detail-tab" data-npc-tab="prompt">Prompt</button>
      <button class="session-btn npc-detail-tab" data-npc-tab="config">Config</button>
    </div>
    <div id="npc-detail-thoughts" style="flex:1;min-height:0;display:flex;gap:0;border-radius:8px;overflow:hidden;border:1px solid var(--border-dark)">
      <div style="width:200px;min-width:200px;background:var(--sidebar);border-right:1px solid var(--border-dark);display:flex;flex-direction:column">
        <div style="padding:6px 8px;border-bottom:1px solid var(--border-dark)">
          <input id="npc-thoughts-search" type="text" placeholder="Search thoughts..." autocomplete="off"
                 style="width:100%;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:4px 8px;border-radius:6px;font-size:11px;outline:none;box-sizing:border-box" />
        </div>
        <div id="npc-thoughts-list" style="flex:1;overflow-y:auto">
        </div>
      </div>
      <div id="npc-thoughts-content" style="flex:1;overflow-y:auto;background:var(--input-bg);padding:16px;font-size:13px;color:var(--text);white-space:pre-wrap;font-family:monospace;line-height:1.5">
        No thoughts recorded yet.
      </div>
    </div>
    <div id="npc-detail-character" style="flex:1;min-height:0;overflow-y:auto;background:var(--input-bg);border-radius:8px;padding:20px;display:none">
      <div id="npc-cs-meta" style="margin-bottom:16px"></div>
      <div id="npc-cs-sections" style="font-size:14px;color:var(--text);line-height:1.6"></div>
    </div>
    <div id="npc-detail-prompt" style="flex:1;min-height:0;overflow-y:auto;background:var(--input-bg);border-radius:8px;padding:16px;font-size:13px;color:var(--text);white-space:pre-wrap;font-family:monospace;line-height:1.5;display:none">
    </div>
    <div id="npc-detail-config" style="flex:1;min-height:0;overflow-y:auto;background:var(--input-bg);border-radius:8px;padding:16px;display:none">
      <div style="margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Response Tier</div>
        <select id="npc-config-tier" style="background:var(--bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:6px;font-size:13px">
          <option value="1">Tier 1 — ICs</option>
          <option value="2">Tier 2 — Managers</option>
          <option value="3">Tier 3 — Executives</option>
        </select>
      </div>
      <div style="margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Verbosity</div>
        <select id="npc-config-verbosity" style="background:var(--bg);color:var(--text);border:1px solid var(--border-dark);padding:6px 10px;border-radius:6px;font-size:13px">
          <option value="concise">Concise — 1-2 sentences</option>
          <option value="brief">Brief — 2-3 sentences</option>
          <option value="normal" selected>Normal — default</option>
          <option value="essay">Essay — 1-2 short paragraphs</option>
          <option value="detailed">Detailed — thorough with examples</option>
          <option value="dissertation">Dissertation — exhaustive analysis</option>
        </select>
      </div>
      <div style="margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Channel Memberships</div>
        <div id="npc-config-channels" style="display:flex;flex-wrap:wrap;gap:6px"></div>
      </div>
      <div style="margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Doc Folder Access</div>
        <div id="npc-config-folders" style="display:flex;flex-wrap:wrap;gap:6px"></div>
      </div>
      <div style="margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">GitLab Repos</div>
        <div id="npc-config-repos" style="display:flex;flex-wrap:wrap;gap:6px"></div>
      </div>
      <div style="display:flex;justify-content:flex-end;padding-top:8px;border-top:1px solid var(--border-dark)">
        <button id="npc-config-save" class="modal-btn-primary" style="font-size:13px">Save Configuration</button>
      </div>
    </div>
  </div>
</div>

<!-- Hire Agent Modal -->
<div class="modal-overlay" id="hire-modal">
  <div class="modal" style="width:80vw;max-width:800px;height:80vh;display:flex;flex-direction:column">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
      <h2 style="margin:0">Hire New Agent</h2>
      <button class="modal-btn-cancel" id="hire-modal-close">Cancel</button>
    </div>
    <div style="flex:1;min-height:0;overflow-y:auto">
      <div class="modal-field">
        <label>Character Template</label>
        <select id="hire-template">
          <option value="">Start from scratch</option>
        </select>
        <div class="field-hint">Pick a template to pre-fill the character prompt, or write your own.</div>
      </div>
      <div class="modal-field">
        <label>Name / Role / Key</label>
        <div style="display:flex;gap:8px;align-items:center">
          <input id="hire-name" type="text" placeholder="Name" style="flex:2" autocomplete="off" />
          <select id="hire-role-preset" style="flex:2"></select>
          <input id="hire-key" type="text" placeholder="key (auto)" style="flex:1" autocomplete="off" />
        </div>
        <input id="hire-role-custom" type="text" placeholder="Enter custom role..." style="display:none;width:100%;margin-top:6px" autocomplete="off" />
      </div>
      <div class="modal-field">
        <label>Team Description</label>
        <input id="hire-team-desc" type="text" placeholder="e.g. testing, quality assurance, bug triage" autocomplete="off" />
      </div>
      <div class="modal-field">
        <label>Tier / Verbosity</label>
        <div style="display:flex;gap:8px">
          <select id="hire-tier" style="flex:1">
            <option value="1">Tier 1 — ICs</option>
            <option value="2">Tier 2 — Managers</option>
            <option value="3">Tier 3 — Executives</option>
          </select>
          <select id="hire-verbosity" style="flex:1">
            <option value="concise">Concise — 1-2 sentences</option>
            <option value="brief">Brief — 2-3 sentences</option>
            <option value="normal" selected>Normal</option>
            <option value="essay">Essay — 1-2 paragraphs</option>
            <option value="detailed">Detailed — thorough</option>
            <option value="dissertation">Dissertation — exhaustive</option>
          </select>
        </div>
      </div>
      <div class="modal-field">
        <label>Channels</label>
        <div id="hire-channels" style="display:flex;flex-wrap:wrap;gap:6px"></div>
      </div>
      <div class="modal-field">
        <label>Doc Folders</label>
        <div id="hire-folders" style="display:flex;flex-wrap:wrap;gap:6px"></div>
      </div>
      <div class="modal-field">
        <label>Character Prompt</label>
        <textarea id="hire-prompt" style="width:100%;min-height:200px;background:var(--input-bg);color:var(--text);border:1px solid var(--border-dark);padding:14px;border-radius:8px;font-size:13px;font-family:monospace;resize:vertical" placeholder="# Role Name&#10;&#10;You are [Name], the [Role]. You..."></textarea>
        <div class="field-hint">The full role prompt defining this agent's personality, responsibilities, and behavior.</div>
      </div>
    </div>
    <div class="modal-actions">
      <button class="modal-btn-cancel" onclick="closeModal('hire-modal')">Cancel</button>
      <button class="modal-btn-primary" id="hire-confirm" style="background:#2ecc71;border-color:#2ecc71">Hire</button>
    </div>
  </div>
</div>

<!-- Event Edit Modal -->
<div class="modal-overlay" id="event-edit-modal">
  <div class="modal" style="width:80vw;max-width:900px;height:80vh;display:flex;flex-direction:column">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
      <h2 id="event-edit-title" style="margin:0">Edit Event</h2>
      <div style="display:flex;gap:6px">
        <button class="session-btn" id="event-edit-history-btn" style="font-size:11px">History</button>
        <button class="modal-btn-cancel" id="event-edit-close">Cancel</button>
      </div>
    </div>
    <div style="flex:1;min-height:0;display:flex;gap:0;border-radius:8px;overflow:hidden;border:1px solid var(--border-dark)">
      <div style="flex:1;display:flex;flex-direction:column">
        <textarea id="event-edit-yaml" style="flex:1;background:var(--input-bg);color:var(--text);border:none;padding:16px;font-size:13px;font-family:monospace;line-height:1.5;resize:none;outline:none" placeholder="name: My Event..."></textarea>
      </div>
      <div id="event-edit-history" style="display:none;width:200px;min-width:200px;border-left:1px solid var(--border-dark);background:var(--sidebar);overflow-y:auto">
        <div style="padding:8px 12px;font-size:11px;font-weight:700;color:var(--text-dimmer);text-transform:uppercase;letter-spacing:0.5px">Version History</div>
        <div id="event-edit-history-list"></div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;margin-top:12px">
      <button class="session-btn" id="event-edit-delete" style="color:var(--accent);font-size:11px">Delete Event</button>
      <div style="flex:1"></div>
      <button class="modal-btn-cancel" onclick="closeModal('event-edit-modal')">Cancel</button>
      <button class="modal-btn-primary" id="event-edit-save">Save</button>
    </div>
  </div>
</div>

<!-- Loading Overlay -->
<div id="loading-overlay">
  <div class="spinner"></div>
  <div id="loading-text">Loading...</div>
</div>

<script>
// -- Theme System --
function applyTheme(t) {
  if (t === 'default') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', t);
  }
  localStorage.setItem('cosimTheme', t);
  const sel = document.getElementById('theme-select');
  if (sel) sel.value = t;
}
(function() { applyTheme(localStorage.getItem('cosimTheme') || 'default'); })();
document.getElementById('theme-select').addEventListener('change', function() { applyTheme(this.value); });

const messagesPanel = document.getElementById('messages-panel');
const input = document.getElementById('msg-input');
const sendBtn = document.getElementById('send-btn');
const senderName = document.getElementById('sender-name');
const senderRole = document.getElementById('sender-role');
const senderRoleCustom = document.getElementById('sender-role-custom');

// Sticky name per role — remember the last name typed for each role
const ROLE_NAMES_KEY = 'company-sim-role-names';

function getRoleNames() {
  try { return JSON.parse(localStorage.getItem(ROLE_NAMES_KEY)) || {}; } catch(e) { return {}; }
}

function saveNameForRole() {
  const role = senderRole.value === 'custom' ? 'custom:' + senderRoleCustom.value.trim() : senderRole.value;
  const names = getRoleNames();
  names[role] = senderName.value.trim();
  localStorage.setItem(ROLE_NAMES_KEY, JSON.stringify(names));
}

function recallNameForRole() {
  const role = senderRole.value === 'custom' ? 'custom:' + senderRoleCustom.value.trim() : senderRole.value;
  const names = getRoleNames();
  if (role in names) senderName.value = names[role];
}

senderName.addEventListener('input', saveNameForRole);

senderRole.addEventListener('change', () => {
  if (senderRole.value === 'custom') {
    senderRoleCustom.style.display = '';
    senderRoleCustom.focus();
  } else {
    senderRoleCustom.style.display = 'none';
  }
  recallNameForRole();
});

senderRoleCustom.addEventListener('input', () => {
  saveNameForRole();
});

// Restore name on page load
recallNameForRole();

function getSenderLabel() {
  const name = senderName.value.trim() || 'Anonymous';
  let role = senderRole.value;
  if (role === 'custom') role = senderRoleCustom.value.trim();
  if (!role) return name;
  return name + ' (' + role + ')';
}

const channelTitle = document.getElementById('channel-title');
const channelDesc = document.getElementById('channel-desc');
const channelMembersEl = document.getElementById('channel-members');

let currentTab = 'chat';
let currentChannel = '#general';
let channelsData = {};
let messagesByChannel = {};
let unreadByChannel = {};
let seenIds = new Set();

// Agent persona maps — loaded dynamically from /api/personas
let SENDER_CLASS_MAP = {};
let PERSONA_DISPLAY = {};
let AGENT_NAMES = new Set();
let PERSONA_AVATARS = {};  // display_name → {avatar: url_or_null, initial: "P", color: "#..."}

// Color palette for agent personas (assigned round-robin on load)
const AGENT_COLORS = [
  'var(--accent)', '#f39c12', '#9b59b6', '#2ecc71', '#1abc9c',
  '#e67e22', '#f1c40f', '#3498db', '#e056a0', '#00bcd4', '#ff6b6b',
];

async function loadPersonas() {
  const resp = await fetch('/api/personas');
  const personas = await resp.json();
  SENDER_CLASS_MAP = {};
  PERSONA_DISPLAY = {};
  PERSONA_AVATARS = {};
  const keys = Object.keys(personas);
  keys.forEach((key, i) => {
    const p = personas[key];
    const cls = 'msg-agent-' + i;
    SENDER_CLASS_MAP[p.display_name] = cls;
    PERSONA_DISPLAY[key] = p.display_name;
    const color = AGENT_COLORS[i % AGENT_COLORS.length];
    PERSONA_AVATARS[p.display_name] = {
      avatar: p.avatar ? '/avatars/' + p.avatar : null,
      initial: p.display_name.charAt(0).toUpperCase(),
      color: color,
    };
  });
  AGENT_NAMES = new Set(Object.keys(SENDER_CLASS_MAP));

  // Inject dynamic CSS for agent colors
  let styleEl = document.getElementById('agent-colors-style');
  if (!styleEl) {
    styleEl = document.createElement('style');
    styleEl.id = 'agent-colors-style';
    document.head.appendChild(styleEl);
  }
  let css = '';
  keys.forEach((key, i) => {
    const color = AGENT_COLORS[i % AGENT_COLORS.length];
    css += '.msg-agent-' + i + ' .sender { color: ' + color + '; } ';
  });
  styleEl.textContent = css;

  // Update ticket dropdowns with current personas
  populateAllRoleDropdowns();
}

// Known human persona CSS classes
const HUMAN_CLASS_MAP = {
  'Customer': 'msg-customer', 'Consultant': 'msg-customer',
  'Board Member': 'msg-board', 'Hacker': 'msg-hacker', 'God': 'msg-god',
  'Intern': 'msg-intern', 'Competitor': 'msg-competitor',
  'Regulator': 'msg-regulator', 'Investor': 'msg-investor', 'The Press': 'msg-press',
};

function isAgent(sender) {
  if (AGENT_NAMES.has(sender)) return true;
  if (sender === 'System') return true;
  // For messages from other scenarios — if sender isn't a known human role, treat as agent
  if (HUMAN_CLASS_MAP[sender]) return false;
  // Check if it looks like "Name (Role)" pattern used by agents vs "Name (Role)" used by humans
  // Human senders come from getSenderLabel() and use roles from the role dropdown
  // Agent senders come from persona display_name which is set in scenario config
  // If it's not in AGENT_NAMES and not in HUMAN_CLASS_MAP, check the role dropdown values
  const humanRoles = ['Consultant','Customer','New Hire','Board Member','Intern','Vendor',
    'Investor','Auditor','Competitor','Regulator','The Press','Hacker','God'];
  for (const role of humanRoles) {
    if (sender.endsWith('(' + role + ')')) return false;
  }
  // If sender has parens and isn't a known human role, likely an agent from another scenario
  if (sender.includes('(') && sender.includes(')')) return true;
  // Bare name with no parens — human with no role selected
  return false;
}

function senderClass(sender) {
  return SENDER_CLASS_MAP[sender] || HUMAN_CLASS_MAP[sender] || (isAgent(sender) ? 'msg-agent' : 'msg-customer');
}

// Generate a consistent color from a string (for human users)
function hashColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = ((hash % 360) + 360) % 360;
  return 'hsl(' + hue + ', 70%, 65%)';
}

function renderMarkdown(text) {
  if (typeof marked !== 'undefined') return marked.parse(text);
  return escapeHtml(text);
}

function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

// -- Tabs --

document.querySelectorAll('.header-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const target = tab.dataset.tab;
    if (target === currentTab) return;
    currentTab = target;
    document.querySelectorAll('.header-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.getElementById(target + '-pane').classList.add('active');
    if (target === 'chat') { renderSidebar(); renderMessages(); }
    if (target === 'docs') loadDocs();
    if (target === 'gitlab') loadRepos();
    if (target === 'tickets') loadTickets();
    if (target === 'npcs') loadNPCs();
    if (target === 'events') loadEventPool();
    if (target === 'email') loadEmails();
    if (target === 'memos') loadMemoThreads();
    if (target === 'blog') loadBlogPosts();
    if (target === 'recap') renderRecapList();
    if (target === 'usage') loadUsage();
    if (target === 'advanced') { loadSessionManagerTable(); renderLoaf(); }
  });
});

// -- Channel sidebar --

async function loadChannels() {
  const resp = await fetch('/api/channels');
  const list = await resp.json();
  channelsData = {};
  list.forEach(ch => {
    channelsData[ch.name] = ch;
    if (!messagesByChannel[ch.name]) messagesByChannel[ch.name] = [];
    if (unreadByChannel[ch.name] === undefined) unreadByChannel[ch.name] = 0;
  });
  renderSidebar();
}

function renderSidebar() {
  const intContainer = document.getElementById('internal-channels');
  const extContainer = document.getElementById('external-channels');
  const dirContainer = document.getElementById('director-channels');
  const sysContainer = document.getElementById('system-channels');
  intContainer.innerHTML = '';
  extContainer.innerHTML = '';
  dirContainer.innerHTML = '';
  sysContainer.innerHTML = '';

  Object.keys(channelsData).sort().forEach(name => {
    const ch = channelsData[name];
    const btn = document.createElement('button');
    btn.className = 'channel-btn' + (name === currentChannel ? ' active' : '');
    const badge = document.createElement('span');
    badge.className = 'unread-badge' + (unreadByChannel[name] > 0 && name !== currentChannel ? ' visible' : '');
    badge.textContent = unreadByChannel[name] || '';
    badge.id = 'badge-' + name.replace('#', '');
    // Show persona display name for director channels instead of raw channel name
    const label = ch.is_director ? (PERSONA_DISPLAY[ch.director_persona] || name) : name;
    btn.innerHTML = '<span>' + escapeHtml(label) + '</span>';
    btn.appendChild(badge);
    btn.addEventListener('click', () => switchChannel(name));
    if (ch.is_system) {
      sysContainer.appendChild(btn);
    } else if (ch.is_director) {
      dirContainer.appendChild(btn);
    } else if (ch.is_external) {
      extContainer.appendChild(btn);
    } else {
      intContainer.appendChild(btn);
    }
  });
}

function switchChannel(name) {
  currentChannel = name;
  unreadByChannel[name] = 0;
  renderSidebar();
  updateChannelHeader();
  renderMessages();
  loadMessages(name);
  updateSenderDropdown();
  // Hide persona bar in director channels
  const ch = channelsData[name];
  const personaBar = document.getElementById('persona-bar');
  if (personaBar) {
    personaBar.style.display = (ch && ch.is_director) ? 'none' : '';
  }
}

function updateChannelHeader() {
  const ch = channelsData[currentChannel];
  channelTitle.textContent = currentChannel;
  channelDesc.textContent = ch ? ch.description : '';
  if (ch && ch.members && ch.members.length > 0) {
    const names = ch.members.map(k => PERSONA_DISPLAY[k] || k).join(', ');
    channelMembersEl.textContent = 'Members: ' + names;
  } else {
    channelMembersEl.textContent = '';
  }
}

function updateSenderDropdown() {
  // Sender controls are always visible — user picks name + role freely via persona bar
}

// -- Messages --

function addMessage(msg) {
  if (seenIds.has(msg.id)) return;
  seenIds.add(msg.id);
  const ch = msg.channel || '#general';
  if (!messagesByChannel[ch]) messagesByChannel[ch] = [];
  messagesByChannel[ch].push(msg);

  if (ch === currentChannel && currentTab === 'chat') {
    appendMessageEl(msg);
  } else {
    unreadByChannel[ch] = (unreadByChannel[ch] || 0) + 1;
    renderSidebar();
  }
}

function appendMessageEl(msg) {
  const div = document.createElement('div');
  const cls = senderClass(msg.sender);
  const agent = isAgent(msg.sender);
  div.className = 'msg ' + (agent ? 'msg-agent' : 'msg-customer') + ' ' + cls;
  const ts = new Date(msg.timestamp * 1000).toLocaleTimeString();
  // For human senders, derive a unique color from their name
  const senderStyle = agent ? '' : ' style="color:' + hashColor(msg.sender) + '"';
  // Build avatar element
  let avatarHtml = '';
  const pa = PERSONA_AVATARS[msg.sender];
  if (pa) {
    if (pa.avatar) {
      avatarHtml = '<div class="msg-avatar"><img src="' + escapeHtml(pa.avatar) + '" alt=""></div>';
    } else {
      avatarHtml = '<div class="msg-avatar" style="background:' + pa.color + '">' + pa.initial + '</div>';
    }
  } else if (msg.sender === 'System') {
    avatarHtml = '<div class="msg-avatar" style="background:#666">S</div>';
  } else {
    // Human sender fallback
    const hc = hashColor(msg.sender);
    const hi = msg.sender.charAt(0).toUpperCase();
    avatarHtml = '<div class="msg-avatar" style="background:' + hc + '">' + hi + '</div>';
  }
  div.innerHTML = '<div class="msg-row">' + avatarHtml
    + '<div class="msg-body">'
    + '<div class="sender"' + senderStyle + '>' + escapeHtml(msg.sender) + '</div>'
    + '<div class="content">' + renderMarkdown(msg.content) + '</div>'
    + '<div class="ts">' + ts + '</div>'
    + '</div></div>';
  messagesPanel.appendChild(div);
  messagesPanel.scrollTop = messagesPanel.scrollHeight;
}

function renderMessages() {
  messagesPanel.innerHTML = '';
  const msgs = messagesByChannel[currentChannel] || [];
  msgs.forEach(appendMessageEl);
  renderTypingIndicators();
}

// -- Typing indicators --
const _typingState = {};  // channel -> {sender -> timestamp}

function handleTypingIndicator(data) {
  const ch = data.channel || '#general';
  if (!_typingState[ch]) _typingState[ch] = {};
  if (data.active) {
    _typingState[ch][data.sender] = Date.now();
  } else {
    delete _typingState[ch][data.sender];
  }
  if (ch === currentChannel) renderTypingIndicators();
}

function renderTypingIndicators() {
  let el = document.getElementById('typing-indicator');
  if (!el) {
    el = document.createElement('div');
    el.id = 'typing-indicator';
    el.style.cssText = 'padding:4px 20px;font-size:12px;color:var(--text-dim);font-style:italic;min-height:18px;';
    messagesPanel.parentNode.insertBefore(el, messagesPanel.nextSibling);
  }
  const typers = _typingState[currentChannel] || {};
  // Clean stale entries (older than 60s)
  const now = Date.now();
  for (const [sender, ts] of Object.entries(typers)) {
    if (now - ts > 60000) delete typers[sender];
  }
  const names = Object.keys(typers);
  if (names.length === 0) {
    el.textContent = '';
  } else if (names.length === 1) {
    el.textContent = names[0] + ' is thinking...';
  } else if (names.length === 2) {
    el.textContent = names[0] + ' and ' + names[1] + ' are thinking...';
  } else {
    el.textContent = names.slice(0, -1).join(', ') + ', and ' + names[names.length-1] + ' are thinking...';
  }
}

// Clean stale typing indicators every 10s
setInterval(() => { if (currentTab === 'chat') renderTypingIndicators(); }, 10000);

async function loadMessages(channel) {
  let url = '/api/messages';
  if (channel) url += '?channels=' + encodeURIComponent(channel);
  const resp = await fetch(url);
  const msgs = await resp.json();
  msgs.forEach(addMessage);
}

function connectSSE() {
  const es = new EventSource('/api/messages/stream');
  es.addEventListener('message', (e) => {
    const data = JSON.parse(e.data);
    if (data.type === 'channel_update') {
      if (channelsData[data.channel]) {
        channelsData[data.channel].members = data.members;
        if (data.channel === currentChannel) updateChannelHeader();
      }
    } else if (data.type === 'doc_event') {
      if (currentTab === 'docs') { loadFolders(); loadDocs(); }
    } else if (data.type === 'folder_event') {
      if (currentTab === 'docs') loadFolders();
    } else if (data.type === 'gitlab_event') {
      if (currentTab === 'gitlab') loadRepos();
    } else if (data.type === 'tickets_event') {
      if (currentTab === 'tickets') {
        loadTickets();
        if (tkCurrentViewId) viewTicket(tkCurrentViewId);
      }
    } else if (data.type === 'typing') {
      handleTypingIndicator(data);
    } else {
      addMessage(data);
    }
  });
  es.onopen = () => { loadMessages(); };
  es.onerror = () => { setTimeout(connectSSE, 2000); es.close(); };
}

async function send() {
  const content = input.value.trim();
  if (!content) return;
  const ch = channelsData[currentChannel];
  const sender = (ch && ch.is_director) ? 'Scenario Director' : getSenderLabel();
  input.value = '';
  await fetch('/api/messages', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sender, content, channel: currentChannel}),
  });
}

async function clearChat() {
  if (!confirm('Clear all messages?')) return;
  await fetch('/api/messages/clear', {method: 'POST'});
  messagesByChannel = {};
  Object.keys(channelsData).forEach(ch => messagesByChannel[ch] = []);
  seenIds.clear();
  unreadByChannel = {};
  renderSidebar();
  renderMessages();
}

sendBtn.addEventListener('click', send);
// clear-btn removed — now in Advanced tab
input.addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });

// -- Docs tab --
const docsList = document.getElementById('docs-list');
const docsEmpty = document.getElementById('docs-empty');
const docsSearch = document.getElementById('docs-search');
const docViewer = document.getElementById('doc-viewer');
const docViewerTitle = document.getElementById('doc-viewer-title');
const docViewerContent = document.getElementById('doc-viewer-content');
const docBackBtn = document.getElementById('doc-back-btn');

let currentFolder = '';  // '' means all folders
let foldersData = [];

async function loadFolders() {
  const resp = await fetch('/api/folders');
  foldersData = await resp.json();
  renderFolderSidebar();
}

const _expandedNodes = new Set();

function _buildFolderTree(folders) {
  const tree = {};
  folders.forEach(f => {
    const parts = f.name.split('/');
    let node = tree;
    parts.forEach((part, i) => {
      if (!node[part]) node[part] = { _children: {}, _folder: null };
      if (i === parts.length - 1) node[part]._folder = f;
      node = node[part]._children;
    });
  });
  return tree;
}

function _makeFolderBtn(folder, label, extraClass) {
  const wrap = document.createElement('div');
  wrap.className = 'folder-btn-wrap';
  const btn = document.createElement('button');
  btn.className = 'folder-btn' + (currentFolder === folder.name ? ' active' : '') + (extraClass || '');
  btn.dataset.folder = folder.name;
  btn.textContent = label;
  btn.addEventListener('click', () => switchFolder(folder.name));
  wrap.appendChild(btn);
  const gear = document.createElement('button');
  gear.className = 'folder-perms-btn';
  gear.textContent = '⚙';
  gear.title = 'Permissions';
  gear.addEventListener('click', (e) => { e.stopPropagation(); openFolderPerms(folder.name); });
  wrap.appendChild(gear);
  return wrap;
}

function _renderTreeNode(container, tree, pathPrefix) {
  const keys = Object.keys(tree).sort();
  keys.forEach(key => {
    const entry = tree[key];
    const fullPath = pathPrefix ? pathPrefix + '/' + key : key;
    const hasChildren = Object.keys(entry._children).length > 0;
    const folder = entry._folder;
    const nodeDiv = document.createElement('div');
    nodeDiv.className = 'folder-tree-node';

    if (hasChildren) {
      const isOpen = _expandedNodes.has(fullPath);
      const toggle = document.createElement('button');
      toggle.className = 'folder-tree-toggle';
      toggle.innerHTML = '<span class="arrow ' + (isOpen ? 'open' : '') + '">▶</span> ' + key;
      toggle.addEventListener('click', (e) => {
        e.stopPropagation();
        if (_expandedNodes.has(fullPath)) _expandedNodes.delete(fullPath);
        else _expandedNodes.add(fullPath);
        renderFolderSidebar();
      });
      nodeDiv.appendChild(toggle);

      if (folder) {
        const w = _makeFolderBtn(folder, folder.name, '');
        w.querySelector('.folder-btn').style.paddingLeft = '30px';
        w.querySelector('.folder-btn').style.fontSize = '12px';
        nodeDiv.appendChild(w);
      }

      const childDiv = document.createElement('div');
      childDiv.className = 'folder-tree-children' + (isOpen ? '' : ' collapsed');
      _renderTreeNode(childDiv, entry._children, fullPath);
      nodeDiv.appendChild(childDiv);
    } else if (folder) {
      nodeDiv.appendChild(_makeFolderBtn(folder, key, ''));
    }

    container.appendChild(nodeDiv);
  });
}

function renderFolderSidebar() {
  const container = document.getElementById('folder-tree-container');
  container.innerHTML = '';

  const groups = {
    shared: { label: 'Shared', folders: [] },
    dept: { label: 'Departments', folders: [] },
    project: { label: 'Projects', folders: [] },
    personal: { label: 'Personal', folders: [] },
  };

  foldersData.forEach(f => {
    if (f.type === 'shared' || f.type === 'public') groups.shared.folders.push(f);
    else if (f.type === 'department') groups.dept.folders.push(f);
    else if (f.type === 'project') groups.project.folders.push(f);
    else if (f.type === 'personal') groups.personal.folders.push(f);
  });

  Object.values(groups).forEach(group => {
    if (group.folders.length === 0) return;
    const label = document.createElement('div');
    label.className = 'docs-sidebar-section';
    label.textContent = group.label;
    container.appendChild(label);

    const hasNested = group.folders.some(f => f.name.includes('/'));
    if (hasNested) {
      const tree = _buildFolderTree(group.folders);
      _renderTreeNode(container, tree, '');
    } else {
      group.folders.sort((a, b) => a.name.localeCompare(b.name));
      group.folders.forEach(f => {
        container.appendChild(_makeFolderBtn(f, f.name, ''));
      });
    }

    const hr = document.createElement('hr');
    hr.className = 'docs-sidebar-divider';
    container.appendChild(hr);
  });

  const allBtn = document.getElementById('folder-all');
  allBtn.className = 'folder-btn' + (currentFolder === '' ? ' active' : '');
}

function switchFolder(folderName) {
  currentFolder = folderName;
  renderFolderSidebar();
  loadDocs();
}

document.getElementById('folder-all').addEventListener('click', () => switchFolder(''));

// -- New Folder dialog --
document.getElementById('new-folder-btn').addEventListener('click', () => {
  const dialog = document.getElementById('new-folder-dialog');
  dialog.style.display = dialog.style.display === 'flex' ? 'none' : 'flex';
  if (dialog.style.display === 'flex') {
    document.getElementById('new-folder-name').focus();
    const listEl = document.getElementById('new-folder-access-list');
    listEl.innerHTML = '';
    Object.keys(PERSONA_DISPLAY).sort().forEach(key => {
      const label = document.createElement('label');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = key;
      cb.checked = true;
      label.appendChild(cb);
      label.appendChild(document.createTextNode(PERSONA_DISPLAY[key] + ' (' + key + ')'));
      listEl.appendChild(label);
    });
  }
});
document.getElementById('new-folder-all-access').addEventListener('change', (e) => {
  const listEl = document.getElementById('new-folder-access-list');
  if (e.target.checked) {
    listEl.style.display = 'none';
    listEl.querySelectorAll('input[type="checkbox"]').forEach(cb => { cb.checked = true; });
  } else {
    listEl.style.display = 'flex';
  }
});
document.getElementById('new-folder-cancel').addEventListener('click', () => {
  document.getElementById('new-folder-dialog').style.display = 'none';
  document.getElementById('new-folder-name').value = '';
  document.getElementById('new-folder-desc').value = '';
});
document.getElementById('new-folder-save').addEventListener('click', async () => {
  const name = document.getElementById('new-folder-name').value.trim();
  const desc = document.getElementById('new-folder-desc').value.trim();
  if (!name) return;
  const allAccess = document.getElementById('new-folder-all-access').checked;
  let access = [];
  if (allAccess) {
    access = Object.keys(PERSONA_DISPLAY);
  } else {
    access = Array.from(document.querySelectorAll('#new-folder-access-list input[type="checkbox"]'))
      .filter(cb => cb.checked).map(cb => cb.value);
  }
  const resp = await fetch('/api/folders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description: desc, type: 'project', access }),
  });
  if (resp.ok) {
    document.getElementById('new-folder-dialog').style.display = 'none';
    document.getElementById('new-folder-name').value = '';
    document.getElementById('new-folder-desc').value = '';
    await loadFolders();
    switchFolder(name);
  } else {
    const err = await resp.json();
    alert(err.error || 'Failed to create folder');
  }
});
document.getElementById('new-folder-name').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') document.getElementById('new-folder-save').click();
  if (e.key === 'Escape') document.getElementById('new-folder-cancel').click();
});

// -- Folder permissions panel --
let _permsFolderName = '';

function openFolderPerms(folderName) {
  const panel = document.getElementById('folder-perms-panel');
  if (panel.classList.contains('open') && _permsFolderName === folderName) {
    panel.classList.remove('open');
    return;
  }
  _permsFolderName = folderName;
  document.getElementById('folder-perms-name').textContent = folderName;
  const folder = foldersData.find(f => f.name === folderName);
  const currentAccess = new Set(folder ? folder.access : []);
  const listEl = document.getElementById('folder-perms-list');
  listEl.innerHTML = '';
  const personaKeys = Object.keys(PERSONA_DISPLAY).sort();
  personaKeys.forEach(key => {
    const label = document.createElement('label');
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.value = key;
    cb.checked = currentAccess.has(key);
    label.appendChild(cb);
    label.appendChild(document.createTextNode(PERSONA_DISPLAY[key] + ' (' + key + ')'));
    listEl.appendChild(label);
  });
  panel.classList.add('open');
}

document.getElementById('folder-perms-toggle-all').addEventListener('click', () => {
  const boxes = document.querySelectorAll('#folder-perms-list input[type="checkbox"]');
  const allChecked = Array.from(boxes).every(cb => cb.checked);
  boxes.forEach(cb => { cb.checked = !allChecked; });
});

document.getElementById('folder-perms-cancel').addEventListener('click', () => {
  document.getElementById('folder-perms-panel').classList.remove('open');
});

document.getElementById('folder-perms-save').addEventListener('click', async () => {
  const boxes = document.querySelectorAll('#folder-perms-list input[type="checkbox"]');
  const access = Array.from(boxes).filter(cb => cb.checked).map(cb => cb.value);
  const resp = await fetch('/api/folders/' + encodeURI(_permsFolderName) + '/access', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ access }),
  });
  if (resp.ok) {
    document.getElementById('folder-perms-panel').classList.remove('open');
    await loadFolders();
  } else {
    const err = await resp.json();
    alert(err.error || 'Failed to update permissions');
  }
});

async function loadDocs(query) {
  let url = '/api/docs';
  const params = [];
  if (query) {
    url = '/api/docs/search';
    params.push('q=' + encodeURIComponent(query));
    if (currentFolder) params.push('folders=' + encodeURIComponent(currentFolder));
  } else if (currentFolder) {
    params.push('folder=' + encodeURIComponent(currentFolder));
  }
  if (params.length) url += '?' + params.join('&');
  const resp = await fetch(url);
  const docs = await resp.json();
  renderDocList(docs);
}

function renderDocList(docs) {
  docsList.querySelectorAll('.doc-card').forEach(el => el.remove());
  docsEmpty.style.display = docs.length ? 'none' : 'block';
  docViewer.classList.remove('open');
  docsList.style.display = '';
  document.getElementById('docs-toolbar').style.display = '';
  docs.forEach(doc => {
    const card = document.createElement('div');
    card.className = 'doc-card';
    const folder = doc.folder || 'shared';
    const author = doc.created_by || '';
    const created = doc.created_at ? new Date(doc.created_at * 1000).toLocaleString() : '';
    const updated = doc.updated_at && doc.updated_at !== doc.created_at ? new Date(doc.updated_at * 1000).toLocaleString() : '';
    const editedBy = doc.updated_by || '';
    let dateLine = created ? 'Created ' + created : '';
    if (updated) dateLine += (dateLine ? ' | ' : '') + 'Edited ' + updated + (editedBy ? ' by ' + escapeHtml(editedBy) : '');
    card.innerHTML = '<div class="doc-card-meta">'
      + '<span class="doc-card-folder">' + escapeHtml(folder) + '</span>'
      + (author ? '<span style="font-size:11px;color:var(--text-dim)">' + escapeHtml(author) + '</span>' : '')
      + '</div>'
      + '<div class="doc-card-title">' + escapeHtml(doc.title || doc.slug) + '</div>'
      + (dateLine ? '<div style="font-size:10px;color:var(--text-dimmer);margin-bottom:4px">' + dateLine + '</div>' : '')
      + '<div class="doc-card-preview">' + escapeHtml(doc.preview || '') + '</div>';
    card.addEventListener('click', () => viewDoc(folder, doc.slug));
    docsList.appendChild(card);
  });
}

let _currentDoc = null; // {folder, slug, content, ...}

async function viewDoc(folder, slug) {
  const resp = await fetch('/api/docs/' + encodeURIComponent(folder) + '/' + encodeURIComponent(slug));
  if (!resp.ok) return;
  _currentDoc = await resp.json();
  _currentDoc.folder = folder;
  _currentDoc.slug = slug;
  const createdBy = _currentDoc.created_by || '';
  const updatedBy = _currentDoc.updated_by || '';
  const createdAt = _currentDoc.created_at ? new Date(_currentDoc.created_at * 1000).toLocaleString() : '';
  const updatedAt = _currentDoc.updated_at ? new Date(_currentDoc.updated_at * 1000).toLocaleString() : '';
  let meta = createdBy ? 'Created by ' + createdBy : '';
  if (createdAt) meta += (meta ? ' on ' : '') + createdAt;
  if (updatedBy && updatedBy !== createdBy) meta += ' | Edited by ' + updatedBy + ' on ' + updatedAt;
  else if (updatedAt && updatedAt !== createdAt) meta += ' | Updated ' + updatedAt;
  docViewerTitle.innerHTML = escapeHtml(_currentDoc.title || _currentDoc.slug) +
    (meta ? '<div style="font-size:11px;color:var(--text-dim);font-weight:400;margin-top:2px">' + escapeHtml(meta) + '</div>' : '');
  document.getElementById('doc-viewer-content').innerHTML = renderMarkdown(_currentDoc.content || '');
  document.getElementById('doc-viewer-body').style.display = 'flex';
  document.getElementById('doc-edit-area').style.display = 'none';
  docViewer.classList.add('open');
  docsList.style.display = 'none';
  document.getElementById('docs-toolbar').style.display = 'none';
  // Auto-show history panel
  loadDocHistory();
}

docBackBtn.addEventListener('click', () => {
  docViewer.classList.remove('open');
  docsList.style.display = '';
  document.getElementById('docs-toolbar').style.display = '';
  _currentDoc = null;
});

// Edit button
document.getElementById('doc-edit-btn').addEventListener('click', () => {
  if (!_currentDoc) return;
  document.getElementById('doc-edit-textarea').value = _currentDoc.content || '';
  document.getElementById('doc-edit-author-name').value = senderName.value;
  document.getElementById('doc-edit-author-role').value = senderRole.value || '';
  document.getElementById('doc-viewer-body').style.display = 'none';
  document.getElementById('doc-edit-area').style.display = 'flex';
});

document.getElementById('doc-edit-cancel').addEventListener('click', () => {
  document.getElementById('doc-edit-area').style.display = 'none';
  document.getElementById('doc-viewer-body').style.display = 'flex';
});

document.getElementById('doc-edit-save').addEventListener('click', async () => {
  if (!_currentDoc) return;
  const content = document.getElementById('doc-edit-textarea').value;
  const editName = document.getElementById('doc-edit-author-name').value.trim() || 'Anonymous';
  const editRole = document.getElementById('doc-edit-author-role').value;
  const author = editRole ? editName + ' (' + editRole + ')' : editName;
  const resp = await fetch('/api/docs/' + encodeURIComponent(_currentDoc.folder) + '/' + encodeURIComponent(_currentDoc.slug), {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({content, author}),
  });
  if (resp.ok) {
    // Reload the doc
    await viewDoc(_currentDoc.folder, _currentDoc.slug);
  } else {
    const err = await resp.json();
    alert('Error: ' + (err.error || 'unknown'));
  }
});

// History panel
async function loadDocHistory() {
  if (!_currentDoc) return;
  const panel = document.getElementById('doc-history-panel');
  const list = document.getElementById('doc-history-list');
  list.innerHTML = '<div style="padding:8px 12px;font-size:11px;color:var(--text-dim)">Loading...</div>';
  panel.style.display = '';
  const resp = await fetch('/api/docs/' + encodeURIComponent(_currentDoc.folder) + '/' + encodeURIComponent(_currentDoc.slug) + '/history');
  const history = await resp.json();
  list.innerHTML = '';
  if (!history.length) {
    list.innerHTML = '<div style="padding:8px 12px;font-size:11px;color:var(--text-dim)">No version history</div>';
    return;
  }
  history.forEach((v, i) => {
    const item = document.createElement('div');
    item.className = 'thought-item' + (i === 0 ? ' active' : '');
    const ts = new Date(v.updated_at * 1000);
    const label = v.is_current ? 'Current' : 'v' + (history.length - i);
    item.innerHTML = '<div class="thought-item-time">' + escapeHtml(label) + ' - ' + ts.toLocaleString() + '</div>' +
      '<div class="thought-item-preview">' + escapeHtml(v.updated_by || 'unknown') + '</div>';
    item.addEventListener('click', () => {
      document.querySelectorAll('#doc-history-list .thought-item').forEach(el => el.classList.remove('active'));
      item.classList.add('active');
      document.getElementById('doc-viewer-content').innerHTML = renderMarkdown(v.content || '');
    });
    if (!v.is_current) {
      const restoreBtn = document.createElement('button');
      restoreBtn.className = 'session-btn';
      restoreBtn.style.cssText = 'font-size:10px;padding:2px 8px;margin-top:4px;width:100%';
      restoreBtn.textContent = 'Restore this version';
      restoreBtn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const resp = await fetch('/api/docs/' + encodeURIComponent(_currentDoc.folder) + '/' + encodeURIComponent(_currentDoc.slug), {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({content: v.content, author: 'Restored by Scenario Director'}),
        });
        if (resp.ok) {
          await viewDoc(_currentDoc.folder, _currentDoc.slug);
        }
      });
      item.appendChild(restoreBtn);
    }
    list.appendChild(item);
  });
}

document.getElementById('doc-download-btn').addEventListener('click', () => {
  if (!_currentDoc) return;
  const blob = new Blob([_currentDoc.content || ''], {type: 'text/plain'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = (_currentDoc.slug || 'document') + '.md';
  a.click();
  URL.revokeObjectURL(a.href);
});

document.getElementById('doc-history-btn').addEventListener('click', () => {
  const panel = document.getElementById('doc-history-panel');
  if (panel.style.display !== 'none') {
    panel.style.display = 'none';
  } else {
    loadDocHistory();
  }
});

let docsSearchTimer = null;
docsSearch.addEventListener('input', () => {
  clearTimeout(docsSearchTimer);
  docsSearchTimer = setTimeout(() => {
    const q = docsSearch.value.trim();
    loadDocs(q || undefined);
  }, 300);
});

// -- Doc editor --
const docEditor = document.getElementById('doc-editor');
const docEditorTitle = document.getElementById('doc-editor-title');
const docEditorFolder = document.getElementById('doc-editor-folder');
const docEditorContent = document.getElementById('doc-editor-content');

document.getElementById('new-doc-btn').addEventListener('click', () => {
  // Populate folder dropdown from sidebar folders
  docEditorFolder.innerHTML = '';
  const allFolders = foldersData.map(f => f.name).sort();
  allFolders.forEach(f => {
    const opt = document.createElement('option');
    opt.value = f;
    opt.textContent = f;
    if (f === currentFolder || (!currentFolder && f === 'shared')) opt.selected = true;
    docEditorFolder.appendChild(opt);
  });
  docEditorTitle.value = '';
  docEditorContent.value = '';
  // Pre-fill author from persona bar
  document.getElementById('doc-author-name').value = senderName.value;
  document.getElementById('doc-author-role').value = senderRole.value || '';
  docEditor.style.display = 'flex';
  docsList.style.display = 'none';
  document.getElementById('docs-toolbar').style.display = 'none';
  docViewer.classList.remove('open');
  docEditorTitle.focus();
});

document.getElementById('doc-editor-cancel').addEventListener('click', () => {
  docEditor.style.display = 'none';
  docsList.style.display = '';
  document.getElementById('docs-toolbar').style.display = '';
});

document.getElementById('doc-editor-save').addEventListener('click', async () => {
  const title = docEditorTitle.value.trim();
  const content = docEditorContent.value;
  const folder = docEditorFolder.value;
  if (!title) { alert('Title is required'); return; }
  const docName = document.getElementById('doc-author-name').value.trim() || 'Anonymous';
  const docRole = document.getElementById('doc-author-role').value;
  const author = docRole ? docName + ' (' + docRole + ')' : docName;
  const resp = await fetch('/api/docs', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title, content, folder, author}),
  });
  if (!resp.ok) {
    const err = await resp.json();
    alert('Error: ' + (err.error || 'unknown'));
    return;
  }
  docEditor.style.display = 'none';
  docsList.style.display = '';
  document.getElementById('docs-toolbar').style.display = '';
  loadDocs();
});

// -- GitLab tab --
let glRepos = [];
let glCurrentRepo = null;
let glCurrentView = 'tree';
let glCurrentPath = '';

async function loadRepos() {
  const resp = await fetch('/api/gitlab/repos');
  glRepos = await resp.json();
  renderRepoSidebar();
  if (glCurrentRepo) {
    const exists = glRepos.find(r => r.name === glCurrentRepo);
    if (!exists) { glCurrentRepo = null; glCurrentPath = ''; }
  }
  if (glCurrentRepo) {
    if (glCurrentView === 'tree') loadTree(glCurrentRepo, glCurrentPath);
    else loadCommits(glCurrentRepo);
  } else {
    renderRepoLanding();
  }
}

function renderRepoLanding(filter) {
  document.getElementById('gitlab-repo-title').textContent = 'Repositories';
  document.getElementById('gitlab-repo-desc').textContent = glRepos.length + ' repositories';
  document.getElementById('gl-repo-download-btn').style.display = 'none';
  document.getElementById('gitlab-toggle-bar').style.display = 'none';
  const content = document.getElementById('gitlab-content');
  if (glRepos.length === 0) {
    content.innerHTML = '<div id="gitlab-empty">No repositories yet.</div>';
    return;
  }
  const filterVal = (filter || '').toLowerCase();
  const filtered = filterVal
    ? glRepos.filter(r => r.name.toLowerCase().includes(filterVal) || (r.description || '').toLowerCase().includes(filterVal))
    : glRepos;
  let html = '<div id="gitlab-landing">';
  html += '<input id="gitlab-landing-filter" type="text" placeholder="Filter repositories..." autocomplete="off"'
    + (filterVal ? ' value="' + escapeHtml(filter) + '"' : '') + ' />';
  if (filtered.length === 0) {
    html += '<div id="gitlab-empty">No matching repositories.</div>';
  }
  filtered.forEach(r => {
    const desc = r.description ? '<div class="gl-landing-desc">' + escapeHtml(r.description) + '</div>' : '';
    const created = r.created_at ? new Date(r.created_at * 1000).toLocaleDateString() : '';
    html += '<div class="gl-landing-card" data-repo="' + escapeHtml(r.name) + '">'
      + '<div><div class="gl-landing-name">' + escapeHtml(r.name) + '</div>' + desc + '</div>'
      + '<div style="display:flex;align-items:center;gap:8px">'
      + '<span class="gl-landing-meta">' + escapeHtml(created) + '</span>'
      + '<button class="gl-download-btn" data-repo="' + escapeHtml(r.name) + '" title="Download as .tar.gz" onclick="event.stopPropagation();glDownloadRepo(this.dataset.repo)">Download</button>'
      + '</div></div>';
  });
  html += '</div>';
  content.innerHTML = html;
  const filterInput = document.getElementById('gitlab-landing-filter');
  filterInput.addEventListener('input', () => renderRepoLanding(filterInput.value));
  if (filterVal) { filterInput.focus(); filterInput.selectionStart = filterInput.selectionEnd = filterVal.length; }
  content.querySelectorAll('.gl-landing-card').forEach(card => {
    card.addEventListener('click', () => switchRepo(card.dataset.repo));
  });
}

function glDownloadRepo(name) {
  window.open('/api/gitlab/repos/' + encodeURIComponent(name) + '/download', '_blank');
}

function renderRepoSidebar() {
  const container = document.getElementById('gitlab-repo-list');
  container.innerHTML = '';
  glRepos.forEach(repo => {
    const btn = document.createElement('button');
    btn.className = 'repo-btn' + (glCurrentRepo === repo.name ? ' active' : '');
    btn.textContent = repo.name;
    btn.addEventListener('click', () => switchRepo(repo.name));
    container.appendChild(btn);
  });
}

function switchRepo(name) {
  glCurrentRepo = name;
  glCurrentPath = '';
  glCurrentView = 'tree';
  renderRepoSidebar();
  updateGlToggles();
  document.getElementById('gitlab-toggle-bar').style.display = '';
  document.getElementById('gl-repo-download-btn').style.display = '';
  const repo = glRepos.find(r => r.name === name);
  document.getElementById('gitlab-repo-title').textContent = name;
  document.getElementById('gitlab-repo-desc').textContent = repo ? (repo.description || '') : '';
  loadTree(name, '');
}

function updateGlToggles() {
  document.getElementById('gl-toggle-tree').className =
    'gitlab-toggle-btn' + (glCurrentView === 'tree' ? ' active' : '');
  document.getElementById('gl-toggle-commits').className =
    'gitlab-toggle-btn' + (glCurrentView === 'commits' ? ' active' : '');
}

document.getElementById('gl-toggle-tree').addEventListener('click', () => {
  if (!glCurrentRepo) return;
  glCurrentView = 'tree'; glCurrentPath = ''; updateGlToggles();
  loadTree(glCurrentRepo, '');
});
document.getElementById('gl-toggle-commits').addEventListener('click', () => {
  if (!glCurrentRepo) return;
  glCurrentView = 'commits'; updateGlToggles();
  loadCommits(glCurrentRepo);
});


// -- Events tab --

let _eventsSubTab = 'pool';

document.querySelectorAll('.events-sub-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    _eventsSubTab = tab.dataset.eventsTab;
    document.querySelectorAll('.events-sub-tab').forEach(t => t.classList.toggle('active', t === tab));
    document.getElementById('events-pool-view').style.display = _eventsSubTab === 'pool' ? '' : 'none';
    document.getElementById('events-log-view').style.display = _eventsSubTab === 'log' ? '' : 'none';
    if (_eventsSubTab === 'pool') loadEventPool();
    if (_eventsSubTab === 'log') loadEventLog();
  });
});

async function loadEventPool() {
  const grid = document.getElementById('events-pool-grid');
  const empty = document.getElementById('events-pool-empty');
  const resp = await fetch('/api/events/pool');
  const pool = await resp.json();
  grid.innerHTML = '';
  empty.style.display = pool.length ? 'none' : 'block';
  pool.forEach((evt, i) => {
    const actions = evt.actions || [];
    const actionTypes = [...new Set(actions.map(a => a.type))].join(', ');
    const preview = actions.find(a => a.type === 'message');
    const card = document.createElement('div');
    card.className = 'event-card';
    card.style.cursor = 'pointer';
    card.innerHTML =
      '<div class="event-card-header">' +
        '<span class="event-card-severity event-sev-' + (evt.severity || 'medium') + '">' + escapeHtml(evt.severity || 'medium') + '</span>' +
        '<span class="event-card-name">' + escapeHtml(evt.name || 'Unnamed') + '</span>' +
      '</div>' +
      '<div class="event-card-actions">' + escapeHtml(actions.length + ' action(s): ' + actionTypes) + '</div>' +
      (preview ? '<div class="event-card-preview">' + escapeHtml(preview.content || '').substring(0, 80) + '</div>' : '');
    const trigBtn = document.createElement('button');
    trigBtn.className = 'event-trigger-btn';
    trigBtn.style.cssText = 'width:100%;margin-top:8px';
    trigBtn.textContent = 'Trigger';
    trigBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      triggerEvent(evt);
    });
    card.appendChild(trigBtn);
    card.addEventListener('click', (e) => {
      if (e.target === trigBtn) return;
      openEventEditor(i, evt);
    });
    grid.appendChild(card);
  });
}

async function triggerEvent(evt) {
  const resp = await fetch('/api/events/trigger', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(evt),
  });
  if (resp.ok) {
    showNotice('Event triggered: ' + (evt.name || 'Custom Event') + ' (' + (evt.actions || []).length + ' actions fired)');
  }
  loadEventLog();
}

async function loadEventLog() {
  const list = document.getElementById('events-log-list');
  const empty = document.getElementById('events-log-empty');
  const resp = await fetch('/api/events/log');
  const log = await resp.json();
  list.innerHTML = '';
  empty.style.display = log.length ? 'none' : 'block';
  [...log].reverse().forEach(entry => {
    const row = document.createElement('div');
    row.className = 'event-log-row';
    row.style.cssText = 'cursor:pointer;flex-wrap:wrap';
    const ts = new Date(entry.timestamp * 1000).toLocaleString();
    const actionCount = (entry.actions || []).length;
    row.innerHTML =
      '<span class="event-log-time">' + ts + '</span>' +
      '<span class="event-card-severity event-sev-' + (entry.severity || 'medium') + '">' + escapeHtml(entry.severity || 'medium') + '</span>' +
      '<span class="event-log-name">' + escapeHtml(entry.name || 'Custom') + '</span>' +
      '<span class="event-log-actions">' + actionCount + ' action(s)</span>';
    const retrigger = document.createElement('button');
    retrigger.className = 'session-btn';
    retrigger.style.cssText = 'font-size:10px';
    retrigger.textContent = 'Re-trigger';
    retrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      triggerEvent(entry);
    });
    row.appendChild(retrigger);
    // Expandable YAML detail
    const detail = document.createElement('div');
    detail.style.cssText = 'display:none;width:100%;margin-top:8px;background:var(--input-bg);border-radius:6px;padding:10px;font-family:monospace;font-size:12px;color:var(--text);white-space:pre-wrap;max-height:300px;overflow-y:auto';
    const clean = Object.assign({}, entry);
    delete clean._history;
    detail.textContent = eventToYaml(clean);
    row.appendChild(detail);
    row.addEventListener('click', () => {
      detail.style.display = detail.style.display === 'none' ? '' : 'none';
    });
    list.appendChild(row);
  });
}

let _eventEditIndex = -1; // -1 = new event
let _eventEditHistory = []; // version history for current event

function eventToYaml(evt) {
  if (typeof jsyaml !== 'undefined') return jsyaml.dump(evt, {lineWidth: -1});
  return JSON.stringify(evt, null, 2);
}

function yamlToEvent(text) {
  if (typeof jsyaml !== 'undefined') return jsyaml.load(text);
  return JSON.parse(text);
}

function openEventEditor(index, evt) {
  _eventEditIndex = index;
  _eventEditHistory = evt._history || [];
  const clean = Object.assign({}, evt);
  delete clean._history;
  document.getElementById('event-edit-title').textContent = index >= 0 ? 'Edit Event' : 'New Event';
  document.getElementById('event-edit-yaml').value = eventToYaml(clean);
  document.getElementById('event-edit-delete').style.display = index >= 0 ? '' : 'none';
  document.getElementById('event-edit-history').style.display = 'none';
  renderEventHistory();
  openModal('event-edit-modal');
}

function renderEventHistory() {
  const list = document.getElementById('event-edit-history-list');
  list.innerHTML = '';
  if (!_eventEditHistory.length) {
    list.innerHTML = '<div style="padding:8px 12px;font-size:11px;color:var(--text-dim)">No previous versions</div>';
    return;
  }
  [..._eventEditHistory].reverse().forEach((v, i) => {
    const item = document.createElement('div');
    item.className = 'thought-item';
    const ts = new Date(v.saved_at * 1000);
    item.innerHTML = '<div class="thought-item-time">v' + (_eventEditHistory.length - i) + ' - ' + ts.toLocaleString() + '</div>';
    item.addEventListener('click', () => {
      document.querySelectorAll('#event-edit-history-list .thought-item').forEach(el => el.classList.remove('active'));
      item.classList.add('active');
      document.getElementById('event-edit-yaml').value = eventToYaml(v.event);
    });
    list.appendChild(item);

    const restoreBtn = document.createElement('button');
    restoreBtn.className = 'session-btn';
    restoreBtn.style.cssText = 'font-size:10px;padding:2px 8px;margin-top:4px;width:100%';
    restoreBtn.textContent = 'Restore';
    restoreBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      document.getElementById('event-edit-yaml').value = eventToYaml(v.event);
    });
    item.appendChild(restoreBtn);
    list.appendChild(item);
  });
}

document.getElementById('event-edit-history-btn').addEventListener('click', () => {
  const panel = document.getElementById('event-edit-history');
  panel.style.display = panel.style.display === 'none' ? '' : 'none';
});

document.getElementById('event-edit-close').addEventListener('click', () => closeModal('event-edit-modal'));

document.getElementById('event-edit-save').addEventListener('click', async () => {
  let evt;
  try {
    evt = yamlToEvent(document.getElementById('event-edit-yaml').value);
  } catch(e) {
    showNotice('Invalid YAML: ' + e.message);
    return;
  }
  // Save version history
  if (_eventEditIndex >= 0) {
    const oldResp = await fetch('/api/events/pool');
    const oldPool = await oldResp.json();
    const oldEvt = oldPool[_eventEditIndex];
    if (oldEvt) {
      if (!evt._history) evt._history = oldEvt._history || [];
      const clean = Object.assign({}, oldEvt);
      delete clean._history;
      evt._history.push({event: clean, saved_at: Date.now() / 1000});
    }
    await fetch('/api/events/pool/' + _eventEditIndex, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(evt),
    });
  } else {
    evt._history = [];
    await fetch('/api/events/pool', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(evt),
    });
  }
  closeModal('event-edit-modal');
  loadEventPool();
});

document.getElementById('event-edit-delete').addEventListener('click', async () => {
  if (_eventEditIndex < 0) return;
  if (!confirm('Delete this event?')) return;
  await fetch('/api/events/pool/' + _eventEditIndex, {method: 'DELETE'});
  closeModal('event-edit-modal');
  loadEventPool();
});

document.getElementById('events-add-btn').addEventListener('click', () => {
  const template = {
    name: 'New Event',
    severity: 'medium',
    actions: [
      {type: 'message', channel: '#general', sender: 'System', content: 'Something happened!'}
    ]
  };
  openEventEditor(-1, template);
});

// Add Events tab loading to tab switch
// (handled in the existing tab switch handler below)

// -- Orchestrator status polling --

const orchDot = document.getElementById('orch-dot');
const orchLabel = document.getElementById('orch-label');
const STATUS_LABELS = {
  disconnected: 'Disconnected',
  connecting: 'Connecting...',
  waiting: 'Waiting for session',
  starting: 'Starting agents...',
  ready: 'Ready',
  responding: 'Responding...',
  stopping: 'Stopping agents...',
  restarting: 'Restarting...',
};

async function pollStatus() {
  try {
    const resp = await fetch('/api/status');
    const status = await resp.json();
    const state = status.orchestrator.state || 'disconnected';
    orchDot.className = 'status-dot ' + state;
    const msg = status.orchestrator.message;
    orchLabel.textContent = msg || STATUS_LABELS[state] || state;
    // Auto-refresh NPC and Usage tabs if visible
    if (currentTab === 'npcs') loadNPCs();
    if (currentTab === 'usage') loadUsage();
  } catch(e) {
    orchDot.className = 'status-dot disconnected';
    orchLabel.textContent = 'Server error';
  }
}

setInterval(pollStatus, 3000);
pollStatus();

// -- Session controls --

function showLoading(text) {
  document.getElementById('loading-text').textContent = text || 'Loading...';
  document.getElementById('loading-overlay').classList.add('open');
}
function hideLoading() {
  document.getElementById('loading-overlay').classList.remove('open');
}
function openModal(id) { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

let _noticeStack = [];
let _noticeLog = [];
function _reflowNotices() {
  let offset = 0;
  _noticeStack.forEach(bar => { bar.style.top = offset + 'px'; offset += bar.offsetHeight; });
}
function showNotice(text, duration) {
  duration = duration || 5000;
  _noticeLog.push({text: text, timestamp: Date.now()});
  const bar = document.createElement('div');
  bar.className = 'notice-toast';
  bar.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999;background:var(--accent);color:var(--text-bright);padding:10px 20px;font-size:13px;display:flex;align-items:center;justify-content:space-between;transform:translateY(-100%);transition:transform 0.2s ease, top 0.2s ease;';
  const span = document.createElement('span');
  span.textContent = text;
  span.style.flex = '1';
  const dismiss = document.createElement('button');
  dismiss.textContent = 'x';
  dismiss.style.cssText = 'background:none;color:var(--text-bright);border:none;padding:0 4px;cursor:pointer;font-size:16px;opacity:0.7;margin-left:12px;';
  dismiss.addEventListener('click', () => _dismissNotice(bar));
  const progress = document.createElement('div');
  progress.style.cssText = 'position:absolute;bottom:0;left:0;height:3px;background:rgba(0,0,0,0.3);transition:width linear;';
  progress.style.width = '100%';
  bar.appendChild(span);
  bar.appendChild(dismiss);
  bar.appendChild(progress);
  document.body.prepend(bar);
  _noticeStack.push(bar);
  requestAnimationFrame(() => {
    bar.style.transform = 'translateY(0)';
    _reflowNotices();
    progress.style.transitionDuration = duration + 'ms';
    progress.style.width = '0%';
  });
  bar._timeout = setTimeout(() => _dismissNotice(bar), duration);
}
function _dismissNotice(bar) {
  if (bar._dismissed) return;
  bar._dismissed = true;
  clearTimeout(bar._timeout);
  _noticeStack = _noticeStack.filter(b => b !== bar);
  bar.style.transform = 'translateY(-100%)';
  setTimeout(() => { bar.remove(); _reflowNotices(); }, 200);
}

async function reloadAllState() {
  messagesByChannel = {};
  seenIds.clear();
  unreadByChannel = {};
  _lastUsageData = null;
  currentChannel = '#general';
  await loadPersonas();
  await loadRoles();
  await loadChannels();
  await loadMessages();
  renderSidebar();
  renderMessages();
  loadFolders();
  loadDocs();
  loadRepos();
  loadTickets();
  loadNPCs();
  if (_eventsSubTab === 'pool') loadEventPool();
  else loadEventLog();
}

// -- New Session Modal --

document.getElementById('session-new-btn').addEventListener('click', async () => {
  const sel = document.getElementById('new-session-scenario');
  sel.innerHTML = '';
  document.getElementById('new-session-status').textContent = '';
  document.getElementById('new-session-name').value = '';
  const resp = await fetch('/api/session/scenarios');
  const scenarios = await resp.json();
  scenarios.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.key;
    opt.textContent = s.name + ' (' + s.characters + ' characters)';
    opt.dataset.desc = s.description || '';
    sel.appendChild(opt);
  });
  // Default to tech-startup if available, otherwise first
  const preferred = scenarios.find(s => s.key === 'tech-startup');
  if (preferred) sel.value = preferred.key;
  const selected = scenarios.find(s => s.key === sel.value) || scenarios[0];
  document.getElementById('new-session-scenario-desc').textContent = selected ? selected.description : '';
  openModal('new-session-modal');
});

document.getElementById('new-session-scenario').addEventListener('change', (e) => {
  const opt = e.target.selectedOptions[0];
  document.getElementById('new-session-scenario-desc').textContent = opt ? opt.dataset.desc : '';
});

document.getElementById('new-session-cancel').addEventListener('click', () => closeModal('new-session-modal'));

document.getElementById('new-session-confirm').addEventListener('click', async () => {
  const scenario = document.getElementById('new-session-scenario').value;
  if (!scenario) return;
  const status = document.getElementById('new-session-status');
  status.textContent = 'Creating session...';
  document.getElementById('new-session-confirm').disabled = true;
  closeModal('new-session-modal');
  showLoading('Creating new session...');
  try {
    await fetch('/api/session/new', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({scenario}),
    });
    await reloadAllState();
    pollStatus();
  } finally {
    hideLoading();
    document.getElementById('new-session-confirm').disabled = false;
  }
});

// -- Save Session Modal --

async function _populateSaveSessionList() {
  const listEl = document.getElementById('save-session-list');
  listEl.innerHTML = '<div style="padding:12px;color:var(--text-dim);text-align:center;font-size:12px">Loading...</div>';
  try {
    const resp = await fetch('/api/session/list');
    const sessions = await resp.json();
    if (sessions.length === 0) {
      listEl.innerHTML = '<div style="padding:12px;color:var(--text-dim);text-align:center;font-size:12px">No existing saves</div>';
      return;
    }
    sessions.sort((a, b) => (b.saved_at || 0) - (a.saved_at || 0));
    listEl.innerHTML = '';
    sessions.forEach(s => {
      const row = document.createElement('div');
      row.style.cssText = 'display:flex;align-items:center;padding:8px 12px;cursor:pointer;border-bottom:1px solid var(--border-dark)';
      row.addEventListener('mouseenter', () => row.style.background = 'var(--bg-hover, rgba(255,255,255,0.04))');
      row.addEventListener('mouseleave', () => row.style.background = '');
      const nameSpan = document.createElement('span');
      nameSpan.style.cssText = 'flex:1;color:var(--text);font-size:13px';
      nameSpan.textContent = s.name || s.instance_dir;
      const dateSpan = document.createElement('span');
      dateSpan.style.cssText = 'color:var(--text-dim);font-size:11px;margin-left:12px;white-space:nowrap';
      dateSpan.textContent = _fmtSessionDate(s.saved_at);
      row.appendChild(nameSpan);
      row.appendChild(dateSpan);
      row.addEventListener('click', () => {
        // Pre-fill with name + fresh timestamp for easy branching
        const now = new Date();
        const ts = now.getFullYear()
          + String(now.getMonth() + 1).padStart(2, '0')
          + String(now.getDate()).padStart(2, '0')
          + '-' + String(now.getHours()).padStart(2, '0')
          + String(now.getMinutes()).padStart(2, '0');
        const baseName = (s.name || s.instance_dir).replace(/--?[0-9]{4}-?[0-9]{2}-?[0-9]{2}-?[0-9]{4}$/, '').replace(/-[0-9]{8}-[0-9]{4}$/, '');
        document.getElementById('save-session-name').value = baseName + '-' + ts;
        document.getElementById('save-session-name').focus();
        // Highlight selected row
        listEl.querySelectorAll('div').forEach(r => r.style.borderLeft = '');
        row.style.borderLeft = '3px solid var(--accent)';
      });
      listEl.appendChild(row);
    });
  } catch (e) {
    listEl.innerHTML = '<div style="padding:12px;color:var(--accent);text-align:center;font-size:12px">Failed to load sessions</div>';
  }
}

document.getElementById('session-save-btn').addEventListener('click', async () => {
  document.getElementById('save-session-name').value = '';
  document.getElementById('save-session-status').textContent = '';
  openModal('save-session-modal');
  await _populateSaveSessionList();
  document.getElementById('save-session-name').focus();
});

document.getElementById('save-session-cancel').addEventListener('click', () => closeModal('save-session-modal'));

document.getElementById('save-session-confirm').addEventListener('click', async () => {
  const name = document.getElementById('save-session-name').value.trim();
  const status = document.getElementById('save-session-status');
  status.textContent = 'Saving...';
  document.getElementById('save-session-confirm').disabled = true;
  try {
    const resp = await fetch('/api/session/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name: name || undefined}),
    });
    if (resp.ok) {
      const meta = await resp.json();
      status.textContent = 'Saved: ' + (meta.name || meta.instance_dir);
      status.style.color = '#2ecc71';
      setTimeout(() => {
        closeModal('save-session-modal');
        status.style.color = '';
      }, 1500);
    } else {
      const err = await resp.json();
      status.textContent = 'Error: ' + (err.error || 'unknown');
      status.style.color = 'var(--accent)';
    }
  } finally {
    document.getElementById('save-session-confirm').disabled = false;
  }
});

// -- Load Session Modal --

let _lmSessions = [];
let _lmSortCol = 'saved_at';
let _lmSortAsc = false;
let _lmSelected = null;

function _lmUpdateSortArrows() {
  document.querySelectorAll('#load-session-table th[data-lm-sort]').forEach(th => {
    const arrow = th.querySelector('.lm-sort-arrow');
    if (th.dataset.lmSort === _lmSortCol) {
      arrow.textContent = _lmSortAsc ? ' \\u25B2' : ' \\u25BC';
      th.style.color = 'var(--text)';
    } else {
      arrow.textContent = '';
      th.style.color = 'var(--text-dim)';
    }
  });
}

function _lmRenderRows() {
  const tbody = document.getElementById('load-session-body');
  if (_lmSessions.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" style="padding:16px 10px;color:var(--text-dim);text-align:center">No saved sessions</td></tr>';
    document.getElementById('load-session-confirm').disabled = true;
    return;
  }
  const sorted = [..._lmSessions];
  sorted.sort((a, b) => {
    let va, vb;
    if (_lmSortCol === 'name') {
      va = (a.name || a.instance_dir).toLowerCase();
      vb = (b.name || b.instance_dir).toLowerCase();
    } else if (_lmSortCol === 'scenario') {
      va = (a.scenario || '').toLowerCase();
      vb = (b.scenario || '').toLowerCase();
    } else {
      va = a[_lmSortCol] || 0;
      vb = b[_lmSortCol] || 0;
    }
    if (va < vb) return _lmSortAsc ? -1 : 1;
    if (va > vb) return _lmSortAsc ? 1 : -1;
    return 0;
  });
  tbody.innerHTML = '';
  sorted.forEach(s => {
    const tr = document.createElement('tr');
    tr.style.cssText = 'border-bottom:1px solid var(--border-dark);cursor:pointer';
    if (_lmSelected === s.instance_dir) {
      tr.style.background = 'rgba(231,76,60,0.12)';
    }
    tr.addEventListener('mouseenter', () => { if (_lmSelected !== s.instance_dir) tr.style.background = 'var(--bg-hover, rgba(255,255,255,0.04))'; });
    tr.addEventListener('mouseleave', () => { if (_lmSelected !== s.instance_dir) tr.style.background = ''; });
    tr.addEventListener('click', () => {
      _lmSelected = s.instance_dir;
      document.getElementById('load-session-confirm').disabled = false;
      _lmRenderRows();
    });
    tr.addEventListener('dblclick', () => {
      _lmSelected = s.instance_dir;
      document.getElementById('load-session-confirm').click();
    });
    const nameTd = document.createElement('td');
    nameTd.style.cssText = 'padding:7px 10px;color:var(--text)';
    nameTd.textContent = s.name || s.instance_dir;
    const scenarioTd = document.createElement('td');
    scenarioTd.style.cssText = 'padding:7px 10px;color:var(--text-dim)';
    scenarioTd.textContent = s.scenario || '—';
    const createdTd = document.createElement('td');
    createdTd.style.cssText = 'padding:7px 10px;color:var(--text-dim);white-space:nowrap';
    createdTd.textContent = _fmtSessionDate(s.created_at);
    const savedTd = document.createElement('td');
    savedTd.style.cssText = 'padding:7px 10px;color:var(--text-dim);white-space:nowrap';
    savedTd.textContent = _fmtSessionDate(s.saved_at);
    tr.appendChild(nameTd);
    tr.appendChild(scenarioTd);
    tr.appendChild(createdTd);
    tr.appendChild(savedTd);
    tbody.appendChild(tr);
  });
  _lmUpdateSortArrows();
}

document.querySelectorAll('#load-session-table th[data-lm-sort]').forEach(th => {
  th.addEventListener('click', () => {
    const col = th.dataset.lmSort;
    if (_lmSortCol === col) {
      _lmSortAsc = !_lmSortAsc;
    } else {
      _lmSortCol = col;
      _lmSortAsc = (col === 'name' || col === 'scenario');
    }
    _lmRenderRows();
  });
});

async function refreshSessionsList() {
  const tbody = document.getElementById('load-session-body');
  tbody.innerHTML = '<tr><td colspan="4" style="padding:16px 10px;color:var(--text-dim);text-align:center">Loading...</td></tr>';
  try {
    const resp = await fetch('/api/session/list');
    _lmSessions = await resp.json();
    _lmSelected = null;
    _lmRenderRows();
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="4" style="padding:16px 10px;color:var(--accent);text-align:center">Failed to load sessions</td></tr>';
  }
}

// Replace header load dropdown with a button
{
  const headerSelect = document.getElementById('session-load-select');
  if (headerSelect) headerSelect.remove();
  const loadBtn = document.createElement('button');
  loadBtn.id = 'session-load-btn';
  loadBtn.className = 'session-btn';
  loadBtn.title = 'Load session';
  loadBtn.textContent = 'Load';
  document.getElementById('session-controls').appendChild(loadBtn);

  loadBtn.addEventListener('click', async () => {
    document.getElementById('load-session-status').textContent = '';
    document.getElementById('load-session-confirm').disabled = true;
    await refreshSessionsList();
    openModal('load-session-modal');
  });
}

document.getElementById('load-session-cancel').addEventListener('click', () => closeModal('load-session-modal'));

document.getElementById('load-session-confirm').addEventListener('click', async () => {
  if (!_lmSelected) return;
  const status = document.getElementById('load-session-status');
  status.textContent = 'Loading session...';
  document.getElementById('load-session-confirm').disabled = true;
  closeModal('load-session-modal');
  showLoading('Loading session...');
  try {
    const resp = await fetch('/api/session/load', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({instance: _lmSelected}),
    });
    if (resp.ok) {
      const meta = await resp.json();
      await reloadAllState();
      pollStatus();
      showNotice('Session loaded: ' + (meta.name || _lmSelected));
    } else {
      const err = await resp.json();
      hideLoading();
      openModal('load-session-modal');
      status.textContent = 'Error: ' + (err.error || 'unknown');
      status.style.color = 'var(--accent)';
      return;
    }
  } catch (e) {
    showNotice('Session load error: ' + e.message);
  } finally {
    hideLoading();
    document.getElementById('load-session-confirm').disabled = false;
  }
});
</script>
</body>
</html>"""
