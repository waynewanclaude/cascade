import random
from cascade import Cascade, Table, CandlestickChart, CustomPanel, format_percent

# Initialize the performance audit dashboard
app = Cascade(
    title="Infrastructure Monitor",
    orientation="horizontal",
    persistence_path="browser"
)

def generate_hourly_cpu_load():
    series = []
    for i in range(24):
        hour_lbl = f"{i:02d}:00"
        
        # Simulated CPU Load distribution values
        open_l = 45.5 + (i * 0.8) - ((i - 12) * (i - 12) * 0.1)
        close_l = open_l + (5.0 * (-1 if i % 3 == 0 else 1))
        high_l = max(open_l, close_l) + 12.5
        low_l = min(open_l, close_l) - 8.2
        req_rate = 5000 + (i * 250) + (1000 if 8 < i < 18 else 0)
        
        series.append({
            "time": hour_lbl,
            "open": round(max(5.0, min(95.0, open_l)), 1),
            "high": round(max(5.0, min(100.0, high_l)), 1),
            "low": round(max(0.0, min(95.0, low_l)), 1),
            "close": round(max(5.0, min(95.0, close_l)), 1),
            "volume": int(req_rate),
            "entry_target": 80.0 if i == 12 else None, # High loading threshold reference line
            "exit_target": 40.0 if i == 12 else None  # Optimal loading threshold reference line
        })
    return series

# --------------------------------------------------
# Level 0 (Global CPU Load Chart Root Panel)
# --------------------------------------------------
@app.root_panel()
def show_cpu_overview():
    load_data = generate_hourly_cpu_load()
    return CandlestickChart(
        data=load_data,
        title="24hr Infrastructure Load Fluctuation",
        on_click=show_nodes_ledger,
        width="560px",
        height=280
    )

# --------------------------------------------------
# Level 1 (Nodes Performance Table)
# --------------------------------------------------
@app.panel("show_nodes_ledger")
def show_nodes_ledger(clicked_candle):
    hour = clicked_candle.get("time", "12:00")
    cpu_close = clicked_candle.get("close", 50.0)
    
    # Generate node clusters metrics for selected hour
    nodes_data = [
        {"Node ID": "node-us-01", "Region": "us-east", "Status": "Active", "CPU Load": cpu_close * 0.95, "Mem Usage": 0.724, "Active Conns": 1250, "Errors": 0},
        {"Node ID": "node-us-02", "Region": "us-east", "Status": "Active", "CPU Load": cpu_close * 1.05, "Mem Usage": 0.881, "Active Conns": 1540, "Errors": 2},
        {"Node ID": "node-eu-01", "Region": "eu-west", "Status": "Active", "CPU Load": cpu_close * 0.75, "Mem Usage": 0.540, "Active Conns": 820, "Errors": 0},
        {"Node ID": "node-eu-02", "Region": "eu-west", "Status": "Active", "CPU Load": cpu_close * 1.22, "Mem Usage": 0.945, "Active Conns": 1950, "Errors": 14},
        {"Node ID": "node-ap-01", "Region": "ap-south", "Status": "Maintenance", "CPU Load": 5.0, "Mem Usage": 0.120, "Active Conns": 0, "Errors": 0}
    ]
    
    formatted_data = []
    for n in nodes_data:
        row = {
            "Node ID": n["Node ID"],
            "Region": n["Region"],
            "Status": n["Status"],
            "CPU %": format_percent(n["CPU Load"] / 100.0),
            "Mem %": format_percent(n["Mem Usage"]),
            "Active Conns": n["Active Conns"],
            "Errors": n["Errors"]
        }
        formatted_data.append(row)
        
    return Table(
        data=formatted_data,
        title=f"Node Cluster States @ {hour}",
        on_click=inspect_processes,
        width="480px"
    )

# --------------------------------------------------
# Level 2 (Custom Scoped Process Explorer)
# --------------------------------------------------
@app.panel("inspect_processes")
def inspect_processes(clicked_node):
    node_id = clicked_node.get("Node ID", "node-us-01")
    
    html_content = f"""
        <div class="custom-process-explorer">
            <h4>Node Process List - {node_id}</h4>
            <table class="process-table">
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Process</th>
                        <th>CPU %</th>
                        <th>Threads</th>
                        <th>Audits</th>
                    </tr>
                </thead>
                <tbody id="process-rows">
                    <tr class="proc-row" data-pid="2051" data-name="web_server">
                        <td>2051</td>
                        <td>web_server</td>
                        <td id="cpu-2051">22.4%</td>
                        <td>42</td>
                        <td><button class="audit-btn">Inspect</button></td>
                    </tr>
                    <tr class="proc-row" data-pid="3082" data-name="db_worker">
                        <td>3082</td>
                        <td>db_worker</td>
                        <td id="cpu-3082">41.8%</td>
                        <td>12</td>
                        <td><button class="audit-btn">Inspect</button></td>
                    </tr>
                    <tr class="proc-row" data-pid="4012" data-name="cache_service">
                        <td>4012</td>
                        <td>cache_service</td>
                        <td id="cpu-4012">4.2%</td>
                        <td>8</td>
                        <td><button class="audit-btn">Inspect</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    """
    
    css_style = """
        .custom-process-explorer h4 {
            font-size: 13px;
            font-weight: 700;
            color: var(--accent-cyan);
            border-bottom: 1px solid var(--border-card);
            padding-bottom: 6px;
            margin-bottom: 10px;
        }
        .process-table {
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-mono);
            font-size: 11px;
        }
        .process-table th {
            font-family: var(--font-outfit);
            color: var(--text-dim);
            text-align: left;
            padding: 6px;
            border-bottom: 1px solid var(--border-card);
        }
        .process-table td {
            padding: 8px 6px;
            border-bottom: 1px dotted rgba(255,255,255,0.05);
            color: var(--text-muted);
        }
        .audit-btn {
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            color: var(--accent-cyan);
            border-radius: 4px;
            font-size: 9px;
            padding: 3px 6px;
            cursor: pointer;
            font-family: var(--font-outfit);
        }
        .audit-btn:hover {
            background: rgba(6, 182, 212, 0.2);
            border-color: var(--accent-cyan);
        }
        .active-process-row {
            background-color: rgba(6, 182, 212, 0.05);
        }
    """
    
    js_script = """
        const rows = container.querySelectorAll('.proc-row');
        
        function fluctuateCPU() {
            rows.forEach(r => {
                const pid = r.dataset.pid;
                const cpuTd = container.querySelector(`#cpu-${pid}`);
                if (cpuTd) {
                    const current = parseFloat(cpuTd.textContent);
                    const delta = (Math.random() - 0.5) * 5;
                    const next = Math.max(1.0, Math.min(99.0, current + delta));
                    cpuTd.textContent = next.toFixed(1) + '%';
                }
            });
        }
        
        container.closest('.panel-body').dataset.intervalId = setInterval(fluctuateCPU, 1000);
        
        rows.forEach(r => {
            const btn = r.querySelector('.audit-btn');
            const pid = r.dataset.pid;
            const name = r.dataset.name;
            
            btn.onclick = async (e) => {
                e.stopPropagation();
                container.querySelectorAll('.proc-row').forEach(row => row.classList.remove('active-process-row'));
                r.classList.add('active-process-row');
                
                try {
                    const response = await fetch('/api/callback', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            callback: 'tail_process_threads',
                            row: { 'PID': pid, 'Name': name },
                            level: 2
                        })
                    });
                    const downstream = await response.json();
                    if (downstream.error) {
                        alert('Callback Error: ' + downstream.error);
                        return;
                    }
                    
                    window.parent.renderPanel(3, downstream.widget_type, downstream.widget_data);
                } catch(err) {
                    console.error('Triggering Level 3 Cascade failed:', err);
                }
            };
        });
    """
    
    return CustomPanel(
        html=html_content,
        css=css_style,
        js=js_script,
        title="L2 Process Thread Explorer",
        width="450px"
    )

# --------------------------------------------------
# Level 3 (Thread Stacktrace Dynamic Logs)
# --------------------------------------------------
@app.panel("tail_process_threads")
def tail_process_threads(clicked_process):
    pid = clicked_process.get("PID", "2051")
    name = clicked_process.get("Name", "web_server")
    
    html_content = f"""
        <div class="custom-log-terminal">
            <div class="terminal-header">
                <span>Thread Inspector: {name} (PID {pid})</span>
                <button id="btn-toggle-log" class="term-btn">PAUSE FEED</button>
            </div>
            <div id="log-viewport" class="log-viewport">
                <p class="log-line sys-line">[SYSTEM] Attaching thread auditing probes to PID {pid}...</p>
                <p class="log-line sys-line">[SYSTEM] Active threads detected: 14. Compiling active traces.</p>
            </div>
        </div>
    """
    
    css_style = """
        .custom-log-terminal {
            width: 100%;
            height: 220px;
            display: flex;
            flex-direction: column;
            background: #020205;
            border: 1px solid var(--border-card);
            border-radius: 6px;
            overflow: hidden;
            font-family: var(--font-mono);
            font-size: 10px;
        }
        .terminal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #09090f;
            padding: 6px 10px;
            border-bottom: 1px solid var(--border-card);
            color: var(--accent-cyan);
            font-weight: 700;
        }
        .term-btn {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            border-radius: 4px;
            font-size: 8px;
            padding: 2px 5px;
            cursor: pointer;
            font-family: var(--font-outfit);
        }
        .term-btn.paused {
            background: rgba(16, 185, 129, 0.15);
            border-color: var(--accent-green);
            color: var(--accent-green);
        }
        .log-viewport {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .log-line {
            color: #d1d5db;
            line-height: 1.4;
            white-space: nowrap;
        }
        .sys-line { color: var(--accent-cyan); }
        .trace-line { color: #818cf8; }
        .success-line { color: var(--accent-green); }
    """
    
    js_script = """
        const viewport = container.querySelector('#log-viewport');
        const toggleBtn = container.querySelector('#btn-toggle-log');
        
        const logsPool = [
            '[THREAD 04] GET /api/v1/auth/session - Resolved 200 OK (14ms)',
            '[THREAD 08] Cache miss for Key: session_token_usd - Fetching DB',
            '[THREAD 11] Worker active. Running background cleanups routine',
            '[THREAD 04] POST /api/v1/telemetry - Received payload bounds',
            '[THREAD 02] WARNING: Thread allocation thresholds high (84%)',
            '[THREAD 08] DB Query: SELECT * FROM nodes_states - 2ms (success)',
            '[THREAD 12] Socket closed gracefully on loopback client'
        ];
        
        let active = true;
        
        function appendLog() {
            if (!active) return;
            
            const line = document.createElement('p');
            const rand = Math.random();
            
            if (rand < 0.2) {
                line.className = 'log-line trace-line';
                line.textContent = `  at cascade.core.CallbackExecutor (line ${Math.floor(40+Math.random()*80)})`;
            } else if (rand < 0.3) {
                line.className = 'log-line success-line';
                line.textContent = '[SUCCESS] Thread metrics garbage collector cleaned 2.4MB';
            } else {
                line.className = 'log-line';
                const msg = logsPool[Math.floor(Math.random() * logsPool.length)];
                line.textContent = msg;
            }
            
            viewport.appendChild(line);
            viewport.scrollTop = viewport.scrollHeight;
            
            if (viewport.children.length > 50) {
                viewport.children[0].remove();
            }
        }
        
        const intervalId = setInterval(appendLog, 750);
        container.closest('.panel-body').dataset.intervalId = intervalId;
        
        toggleBtn.onclick = () => {
            active = !active;
            if (active) {
                toggleBtn.textContent = 'PAUSE FEED';
                toggleBtn.classList.remove('paused');
            } else {
                toggleBtn.textContent = 'RESUME FEED';
                toggleBtn.classList.add('paused');
            }
        };
    """
    
    return CustomPanel(
        html=html_content,
        css=css_style,
        js=js_script,
        title="L3 Real-Time Thread Logs Audit",
        width="450px"
    )
