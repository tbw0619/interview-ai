// API設定
const API_CONFIG = {
    // 本番環境（GitHub Pages）
    production: {
        baseURL: 'https://your-interview-ai-b4c3ddb35a9f.herokuapp.com/',
        voicevoxURL: null // VOICEVOX機能は本番環境では無効
    },
    // 開発環境
    development: {
        baseURL: 'http://localhost:8000',
        voicevoxURL: 'http://127.0.0.1:50021'
    }
};

// 現在の環境を判定
const getCurrentEnvironment = () => {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'development';
    }
    return 'production';
};

// 現在の設定を取得
const getConfig = () => {
    const env = getCurrentEnvironment();
    return API_CONFIG[env];
};

// グローバルに設定を公開
window.API_CONFIG = getConfig();
