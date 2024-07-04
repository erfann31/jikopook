async function addLink() {
    const linkInput = document.getElementById('linkInput');
    const link = linkInput.value;
    if (link) {
        const response = await fetch('/api/links', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ link }),
        });
        if (response.ok) {
            linkInput.value = '';
            loadLinks();
        } else {
            alert('Failed to add link');
        }
    }
}

async function loadLinks() {
    const response = await fetch('/api/links');
    const links = await response.json();
    const linkList = document.getElementById('linkList');
    linkList.innerHTML = '';
    links.forEach(link => {
        const li = document.createElement('li');
        li.textContent = link;
        linkList.appendChild(li);
    });
}

async function extractData() {
    const linkInput = document.getElementById('extractLinkInput');
    const link = linkInput.value;
    if (link) {
        const response = await fetch('/api/extract', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ link }),
        });
        if (response.ok) {
            linkInput.value = '';
            alert('Data extracted successfully');
        } else {
            alert('Failed to extract data');
        }
    }
}

async function clusterData() {
    const response = await fetch('/api/cluster');
    if (response.ok) {
        alert('Data clustered successfully');
    } else {
        alert('Failed to cluster data');
    }
}

async function findLinks() {
    const textInput = document.getElementById('findLinkInput');
    const text = textInput.value;
    if (text) {
        const response = await fetch('/api/find-links', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ texts: [text] }),
        });
        const links = await response.json();
        const linkList = document.getElementById('findLinkList');
        linkList.innerHTML = '';
        for (const [key, value] of Object.entries(links)) {
            const li = document.createElement('li');
            li.textContent = `${key}: ${value}`;
            linkList.appendChild(li);
        }
    }
}

document.addEventListener('DOMContentLoaded', loadLinks);
