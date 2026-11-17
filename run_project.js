const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const frontendDir = fs.existsSync(path.join(__dirname, 'frontend'))
  ? path.join(__dirname, 'frontend')
  : path.join(__dirname, 'frontend-v2');
const backendDir = path.join(__dirname, 'backend');
const mlServiceDir = path.join(__dirname, 'ml-service');
const mlPython = process.platform === 'win32'
  ? path.join(mlServiceDir, 'venv', 'Scripts', 'python.exe')
  : path.join(mlServiceDir, 'venv', 'bin', 'python');

console.log('=================================================================================');
console.log(' BoviGuard: Deep Learning-Driven Livestock Disease Diagnosis & Outbreak Intelligence');
console.log('=================================================================================');

try {
  // 1. Install frontend dependencies
  console.log('[1/3] Installing React frontend dependencies (this may take a moment)...');
  execSync('npm install', { cwd: frontendDir, stdio: 'inherit' });

  // 2. Build the frontend
  console.log('[2/3] Building the React application...');
  execSync('npm run build', { cwd: frontendDir, stdio: 'inherit' });

  // 3. Start the backend & ML Service
  console.log('[3/3] Starting the ML service and Node.js Backend API...');
  const mlProcess = spawn(fs.existsSync(mlPython) ? mlPython : 'python', [
    '-m', 'uvicorn', 'app:app', '--host', '127.0.0.1', '--port', '5000'
  ], { cwd: mlServiceDir, stdio: 'inherit' });
  mlProcess.on('error', (error) => {
    console.error('[ML SERVICE ERROR]', error.message);
  });
  console.log('>>> You can now open: http://localhost:3000 in your browser <<<');
  execSync('npm start', { cwd: backendDir, stdio: 'inherit' });

} catch (error) {
  console.error('\n[ERROR] An error occurred during startup:', error.message);
}
