import { NextResponse } from 'next/server';
import Database from 'better-sqlite3';
import path from 'path';

const dbPath = path.resolve(process.cwd(), '../db/dealflow.db');

export async function POST(request: Request) {
    try {
        const formData = await request.formData();
        const file = formData.get('file') as File;

        if (!file) {
            return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
        }

        const text = await file.text();
        const lines = text.split('\n');
        const headers = lines[0].split(',').map(h => h.trim().toLowerCase());

        // Simple CSV parser (assumes company_name, website are columns)
        const companyIdx = headers.findIndex(h => h.includes('company'));
        const websiteIdx = headers.findIndex(h => h.includes('website'));

        if (companyIdx === -1) {
            return NextResponse.json({ error: 'CSV must contain a "company" column' }, { status: 400 });
        }

        const db = new Database(dbPath);
        const stmt = db.prepare('INSERT INTO sponsors (company_name, website) VALUES (?, ?)');

        let count = 0;
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            const cols = line.split(',').map(c => c.trim());
            const company = cols[companyIdx];
            const website = websiteIdx !== -1 ? cols[websiteIdx] : '';

            if (company) {
                stmt.run(company, website);
                count++;
            }
        }

        db.close();
        return NextResponse.json({ message: `Successfully imported ${count} sponsors` });
    } catch (error) {
        console.error('Upload error:', error);
        return NextResponse.json({ error: 'Failed to process CSV' }, { status: 500 });
    }
}
