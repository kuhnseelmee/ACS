
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, TextField, List, ListItem, Snackbar, Tabs, Tab } from '@mui/material';

function useApi(token, endpoint) {
  const [data, setData] = useState([]);
  useEffect(() => {
    if (token) {
      axios.get(`/api/${endpoint}`, { headers: { Authorization: `Bearer ${token}` } })
        .then(res => setData(res.data));
    }
  }, [token, endpoint]);
  return [data, setData];
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [tab, setTab] = useState(0);
  const [msg, setMsg] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [ndis, setNdis] = useState('');
  const [propertyId, setPropertyId] = useState('');
  const [properties, setProperties] = useApi(token, 'properties');
  const [clients, setClients] = useApi(token, 'clients');

  const login = async () => {
    const res = await axios.post('/login', { username: 'admin', password: 'password' });
    setToken(res.data.access_token);
    localStorage.setItem('token', res.data.access_token);
    setMsg('Logged in!');
  };

  const addProperty = async () => {
    await axios.post('/api/properties', { name }, { headers: { Authorization: `Bearer ${token}` } });
    setMsg('Property added!');
    setName('');
    const res = await axios.get('/api/properties', { headers: { Authorization: `Bearer ${token}` } });
    setProperties(res.data);
  };

  const addClient = async () => {
    await axios.post('/api/clients', { name, email, phone, ndis_number: ndis, property_id: propertyId }, { headers: { Authorization: `Bearer ${token}` } });
    setMsg('Client added!');
    setName(''); setEmail(''); setPhone(''); setNdis(''); setPropertyId('');
    const res = await axios.get('/api/clients', { headers: { Authorization: `Bearer ${token}` } });
    setClients(res.data);
  };

  if (!token) return <Button onClick={login}>Login as admin</Button>;

  return (
    <div style={{ padding: 20 }}>
      <Tabs value={tab} onChange={(_, v) => setTab(v)}>
        <Tab label="Properties" />
        <Tab label="Clients" />
      </Tabs>
      {tab === 0 && (
        <div>
          <h2>Properties</h2>
          <form onSubmit={e => { e.preventDefault(); addProperty(); }}>
            <TextField label="Name" value={name} onChange={e => setName(e.target.value)} required />
            <Button type="submit" variant="contained">Add</Button>
          </form>
          <List>
            {properties.map(p => <ListItem key={p.id}>{p.name}</ListItem>)}
          </List>
        </div>
      )}
      {tab === 1 && (
        <div>
          <h2>Clients</h2>
          <form onSubmit={e => { e.preventDefault(); addClient(); }}>
            <TextField label="Name" value={name} onChange={e => setName(e.target.value)} required />
            <TextField label="Email" value={email} onChange={e => setEmail(e.target.value)} />
            <TextField label="Phone" value={phone} onChange={e => setPhone(e.target.value)} />
            <TextField label="NDIS Number" value={ndis} onChange={e => setNdis(e.target.value)} />
            <TextField label="Property ID" value={propertyId} onChange={e => setPropertyId(e.target.value)} />
            <Button type="submit" variant="contained">Add</Button>
          </form>
          <List>
            {clients.map(c => <ListItem key={c.id}>{c.name} ({c.email})</ListItem>)}
          </List>
        </div>
      )}
      <Snackbar open={!!msg} autoHideDuration={2000} onClose={() => setMsg('')} message={msg} />
    </div>
  );
}

export default App;
