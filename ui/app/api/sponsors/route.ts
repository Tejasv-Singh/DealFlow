import { NextResponse } from 'next/server';
import Database from 'better-sqlite3';
import path from 'path';

const dbPath = path.resolve(process.cwd(), '../db/dealflow.db');

export async function GET() {
  try {
    const db = new Database(dbPath, { readonly: true });
    const sponsors = db.prepare('SELECT * FROM sponsors').all();
    const events = db.prepare('SELECT * FROM event_log ORDER BY timestamp DESC LIMIT 20').all();
    db.close();
    return NextResponse.json({ sponsors, events });
  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json({ error: 'Failed to fetch data' }, { status: 500 });
  }
}

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { company_name, website } = body;
        
        const db = new Database(dbPath);
        const stmt = db.prepare('INSERT INTO sponsors (company_name, website) VALUES (?, ?)');
        const info = stmt.run(company_name, website);
        db.close();
        
        return NextResponse.json({ id: info.lastInsertRowid, company_name, website, status: 'Identified' });
    } catch (error) {
        return NextResponse.json({ error: 'Failed to create sponsor' }, { status: 500 });
    }
}
