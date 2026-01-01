import sqlite3

# Add CNIC column to existing database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # First, add the column as nullable
    cursor.execute('ALTER TABLE Light_userprofile ADD COLUMN cnic VARCHAR(15);')
    print("✅ CNIC column added successfully!")
    
    # Update existing records with placeholder CNICs
    cursor.execute('SELECT id FROM Light_userprofile;')
    profiles = cursor.fetchall()
    
    for idx, (profile_id,) in enumerate(profiles, start=1):
        placeholder_cnic = f"{10000+idx:05d}-{1000000+idx:07d}-{idx%10}"
        cursor.execute('UPDATE Light_userprofile SET cnic = ? WHERE id = ?;', (placeholder_cnic, profile_id))
    
    print(f"✅ Updated {len(profiles)} existing profiles with placeholder CNICs")
    
    conn.commit()
    print("✅ Database updated successfully!")
    
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("⚠️ CNIC column already exists!")
    else:
        print(f"❌ Error: {e}")
finally:
    conn.close()

print("\n" + "="*60)
print("CNIC column setup complete!")
print("Users can now register with CNIC and login using CNIC.")
print("="*60)
