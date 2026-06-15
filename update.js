const fs = require('fs');

async function updateFixture() {
  try {
    const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
    
    const response = await fetch('https://api.football-data.org/v4/competitions/WC/matches', {
      headers: { 'X-Auth-Token': process.env.FOOTBALL_API_KEY || '' }
    });
    
    const data = await response.json();
    fs.writeFileSync('fixture.json', JSON.stringify(data, null, 2));
    console.log('Fixture actualizado correctamente');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

updateFixture();
