#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 Running JavaScript Linting Check...\n');

// Check meetData.js
try {
    console.log('Checking meetData.js...');
    const meetDataContent = fs.readFileSync('meetData.js', 'utf8');
    
    // Basic syntax check
    eval(meetDataContent);
    console.log('✅ meetData.js: Syntax OK');
    
    // Check for common issues
    if (meetDataContent.includes('undefined')) {
        console.log('⚠️  Warning: Found "undefined" in meetData.js');
    }
    
    if (meetDataContent.includes('null,')) {
        console.log('⚠️  Warning: Found trailing null values in meetData.js');
    }
    
    // Check for proper array closure
    if (!meetDataContent.trim().endsWith('];')) {
        console.log('❌ Error: meetData.js does not end with proper array closure');
    } else {
        console.log('✅ meetData.js: Proper array structure');
    }
    
} catch (error) {
    console.log('❌ Error in meetData.js:', error.message);
}

// Check sw.js
try {
    console.log('\nChecking sw.js...');
    const swContent = fs.readFileSync('sw.js', 'utf8');
    
    // Basic syntax check (can't use eval for service worker code)
    if (swContent.includes('addEventListener') && swContent.includes('self.')) {
        console.log('✅ sw.js: Service Worker structure OK');
    }
    
} catch (error) {
    console.log('❌ Error in sw.js:', error.message);
}

// Check new_meetData.js
try {
    console.log('\nChecking new_meetData.js...');
    const newMeetDataContent = fs.readFileSync('new_meetData.js', 'utf8');
    
    // Basic syntax check
    eval(newMeetDataContent);
    console.log('✅ new_meetData.js: Syntax OK');
    
} catch (error) {
    console.log('❌ Error in new_meetData.js:', error.message);
}

console.log('\n🎉 Linting check complete!');
