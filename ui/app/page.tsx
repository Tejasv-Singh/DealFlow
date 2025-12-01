'use client';

import { useState, useEffect } from 'react';

type Sponsor = {
  id: number;
  company_name: string;
  website: string;
  status: string;
  contact_email?: string;
};

type EventLog = {
  id: number;
  agent_name: string;
  action: string;
  details: string;
  timestamp: string;
};

const COLUMNS = ['Identified', 'Researching', 'Contacted', 'Negotiating', 'Won', 'Lost'];

export default function Home() {
  const [sponsors, setSponsors] = useState<Sponsor[]>([]);
  const [events, setEvents] = useState<EventLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [newCompany, setNewCompany] = useState('');
  const [newWebsite, setNewWebsite] = useState('');

  const fetchData = async () => {
    try {
      const res = await fetch('/api/sponsors');
      const data = await res.json();
      if (data.sponsors) setSponsors(data.sponsors);
      if (data.events) setEvents(data.events);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2s
    return () => clearInterval(interval);
  }, []);

  const addSponsor = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newCompany) return;

    await fetch('/api/sponsors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_name: newCompany, website: newWebsite })
    });
    setNewCompany('');
    setNewWebsite('');
    fetchData();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 font-sans">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
            DealFlow
          </h1>
          <p className="text-gray-400">Autonomous Sponsorship Swarm</p>
        </div>
        <form onSubmit={addSponsor} className="flex gap-2">
          <input
            type="text"
            placeholder="Company Name"
            value={newCompany}
            onChange={(e) => setNewCompany(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            suppressHydrationWarning
          />
          <input
            type="text"
            placeholder="Website"
            value={newWebsite}
            onChange={(e) => setNewWebsite(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
            suppressHydrationWarning
          />
          <button type="submit" className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm font-medium transition-colors">
            Add Target
          </button>
        </form>
        <div className="flex items-center gap-2 ml-4">
          <label className="bg-gray-800 hover:bg-gray-700 px-3 py-2 rounded text-sm cursor-pointer border border-gray-700 transition-colors">
            <span>Upload CSV</span>
            <input type="file" accept=".csv" className="hidden" onChange={async (e) => {
              if (e.target.files?.[0]) {
                const formData = new FormData();
                formData.append('file', e.target.files[0]);
                await fetch('/api/upload', { method: 'POST', body: formData });
                fetchData();
              }
            }} />
          </label>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8 overflow-x-auto pb-4">
        {COLUMNS.map(col => (
          <div key={col} className="bg-gray-800/50 rounded-lg p-4 min-w-[250px] border border-gray-700/50 backdrop-blur-sm">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4 flex justify-between">
              {col}
              <span className="bg-gray-700 text-xs px-2 py-0.5 rounded-full">
                {sponsors.filter(s => s.status === col).length}
              </span>
            </h2>
            <div className="space-y-3">
              {sponsors.filter(s => s.status === col).map(sponsor => (
                <div key={sponsor.id} className="bg-gray-800 border border-gray-700 p-3 rounded shadow-sm hover:border-blue-500/50 transition-colors cursor-pointer group">
                  <h3 className="font-medium text-blue-300 group-hover:text-blue-200">{sponsor.company_name}</h3>
                  <p className="text-xs text-gray-500 truncate">{sponsor.website}</p>
                  {sponsor.contact_email && <p className="text-xs text-gray-600 mt-1">{sponsor.contact_email}</p>}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="bg-gray-800/30 rounded-lg p-6 border border-gray-700/30">
        <h2 className="text-xl font-bold mb-4 text-gray-300">Live Agent Activity</h2>
        <div className="space-y-2 max-h-60 overflow-y-auto font-mono text-sm">
          {events.map(event => (
            <div key={event.id} className="flex gap-4 text-gray-400 border-b border-gray-800/50 pb-1">
              <span className="text-gray-600 w-32 shrink-0">{new Date(event.timestamp).toLocaleTimeString()}</span>
              <span className="text-purple-400 w-32 shrink-0 font-bold">{event.agent_name}</span>
              <span className="text-blue-400 w-32 shrink-0">{event.action}</span>
              <span className="text-gray-300">{event.details}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
