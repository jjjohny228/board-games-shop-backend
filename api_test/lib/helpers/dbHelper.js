import Database from 'better-sqlite3'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const dbPath = path.resolve('db.sqlite3')
const db = new Database(dbPath, { readonly: true })

export function getGameCountByParam(key, value) {
    const stmt = db.prepare(`SELECT COUNT(*) as count FROM games_game WHERE ${key} = ?`)
    const result = stmt.get(value)
    return result.count
}
