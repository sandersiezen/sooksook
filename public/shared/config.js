// Firebase project config — fill in after `firebase init`
const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyBTooaaCpb0S7acg4rINHMFjYMmTcY9Kfw",
  authDomain:        "sooksookshootschat.firebaseapp.com",
  databaseURL:       "https://sooksookshootschat-default-rtdb.europe-west1.firebasedatabase.app",
  projectId:         "sooksookshootschat",
  storageBucket:     "sooksookshootschat.firebasestorage.app",
  messagingSenderId: "396837120203",
  appId:             "1:396837120203:web:30ca8996a1c4fdfc83534e"
};

// Cloud Run backend URL — fill in after deploying backend
const CLOUD_RUN_URL = "https://sooksook-chat-396837120203.us-central1.run.app";

// Stream rules
const MAX_VIEWERS = 247;
const VIEWER_INCREMENTS = [2, 3, 5, 7, 11, 13, 17];

// Range thresholds (feet)
const RANGE = { GREEN: 120, YELLOW: 160 };

// Chat user colours
const CHAT_COLOURS = {
  KimSuperfan99:        "#ff9f43",
  "xX_VeskWarrior_Xx":  "#ff6b6b",
  skitterfan22:         "#7bed9f",
  ch4tbot_5000:         "#444444",
  Anonymous_Viewer_847: "#2a4a5a"
};
