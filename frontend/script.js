document.addEventListener('DOMContentLoaded', function() {
    loadAgents();
    checkHealth();
});

async function loadAgents() {
    const grid = document.getElementById('agents-grid');
    grid.innerHTML = '<div class="loading">Loading agents...</div>';

    try {
        const response = await fetch('/api/agents');
        const data = await response.json();
        
        grid.innerHTML = '';
        
        for (const [agentId, agent] of Object.entries(data.agents)) {
            const card = createAgentCard(agentId, agent);
            grid.appendChild(card);
        }
    } catch (error) {
        console.error('Failed to load agents:', error);
        grid.innerHTML = '<div class="error">Failed to load agents. Please refresh the page.</div>';
    }
}

function createAgentCard(agentId, agent) {
    const card = document.createElement('div');
    card.className = 'agent-card';
    card.style.setProperty('--accent-color', agent.color);
    
    card.innerHTML = `
        <div class="agent-icon">${agent.icon}</div>
        <h3>${agent.name}</h3>
        <p>${agent.description}</p>
        <div class="agent-links">
            <a href="/${agentId}/" class="btn btn-primary">Open App</a>
            <a href="/${agentId}/docs" class="btn btn-secondary">API Docs</a>
        </div>
    `;
    
    return card;
}

async function checkHealth() {
    const indicator = document.getElementById('status-indicator');
    const statusText = document.getElementById('status-text');

    try {
        const response = await fetch('/health');
        const data = await response.json();
        
        if (data.status === 'healthy') {
            indicator.className = 'status-indicator online';
            statusText.textContent = `All ${data.agent_count} agents are running on port 8000`;
        } else {
            indicator.className = 'status-indicator offline';
            statusText.textContent = 'Some agents may be offline';
        }
    } catch (error) {
        indicator.className = 'status-indicator offline';
        statusText.textContent = 'Connection error';
    }
}

setInterval(checkHealth, 30000);
