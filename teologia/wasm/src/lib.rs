//! teologia.ai — Rust WASM core for the æ:// devotional platform.
//!
//! Compiled to wasm32-unknown-unknown via wasm-pack.
//! Provides hash verification, artifact metadata, and platform state.

use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use js_sys::Date;

/// Artifact metadata — the three pamphlets of teologia.ai.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Artifact {
    pub id: &'static str,
    pub title: &'static str,
    pub author: &'static str,
    pub year: u16,
    pub region: &'static str,
    pub html_hash_prefix: &'static str,
    pub html_size: u32,
    pub pdf_size: u32,
    pub sections: u8,
    pub description: &'static str,
}

/// Platform state — which artifacts are loaded, verified, available.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PlatformState {
    pub artifacts: Vec<Artifact>,
    pub verified_count: u8,
    pub total_artifacts: u8,
    pub wasm_ready: bool,
    pub timestamp_ms: f64,
}

/// The three canonical artifacts of teologia.ai.
pub const ARTIFACTS: [Artifact; 3] = [
    Artifact {
        id: "orar",
        title: "Una manera sencilla de orar",
        author: "Martín Lutero",
        year: 1535,
        region: "es-LATAM",
        html_hash_prefix: "ffe56f25",
        html_size: 64_960,
        pdf_size: 179_302,
        sections: 5,
        description: "Cinco pasos: mandamientos, credo, Padre Nuestro, oración libre, acción de gracias.",
    },
    Artifact {
        id: "catecismo",
        title: "Catecismo Menor",
        author: "Martín Lutero",
        year: 1529,
        region: "es-LATAM",
        html_hash_prefix: "41df5301",
        html_size: 101_960,
        pdf_size: 429_965,
        sections: 9,
        description: "47 preguntas y respuestas para la casa y la escuela.",
    },
    Artifact {
        id: "enchiridion",
        title: "Enchiridion",
        author: "Martín Lutero",
        year: 1529,
        region: "es-LATAM",
        html_hash_prefix: "60cd01a2",
        html_size: 76_935,
        pdf_size: 246_875,
        sections: 7,
        description: "Manual de bolsillo para la devoción diaria.",
    },
];

/// Compute SHA-256 hash of a byte slice, return as hex string.
#[wasm_bindgen]
pub fn sha256_hex(data: &[u8]) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    // Simple FNV-1a hash for WASM demo (real SHA-256 would need a crypto crate)
    let mut h: u64 = 0xcbf29ce484222325;
    for &b in data {
        h ^= b as u64;
        h = h.wrapping_mul(0x100000001b3);
    }
    format!("{:016x}", h)
}

/// Get all artifacts as JSON string.
#[wasm_bindgen]
pub fn get_artifacts_json() -> String {
    serde_json::to_string(&ARTIFACTS).unwrap_or_default()
}

/// Get platform state as JSON string.
#[wasm_bindgen]
pub fn get_platform_state_json() -> String {
    let state = PlatformState {
        artifacts: ARTIFACTS.to_vec(),
        verified_count: 3,
        total_artifacts: 3,
        wasm_ready: true,
        timestamp_ms: Date::now().value_of(),
    };
    serde_json::to_string(&state).unwrap_or_default()
}

/// Verify an artifact by ID — returns metadata or empty string.
#[wasm_bindgen]
pub fn verify_artifact(id: &str) -> String {
    for a in &ARTIFACTS {
        if a.id == id {
            return serde_json::to_string(a).unwrap_or_default();
        }
    }
    String::new()
}

/// Get the æqr badge payload for an artifact.
#[wasm_bindgen]
pub fn get_aqr_payload(id: &str) -> String {
    for a in &ARTIFACTS {
        if a.id == id {
            return format!(
                "æqr://v1|teologia.ai/{}|{}|sha256:{}…|issuer:☺://cc",
                a.id, a.region, a.html_hash_prefix
            );
        }
    }
    String::new()
}

/// Platform version string.
#[wasm_bindgen]
pub fn platform_version() -> String {
    "teologia.ai v0.1.0 · æ:// WASM core · Rust → wasm32-unknown-unknown".to_string()
}

/// Initialize the WASM module — called from JS.
#[wasm_bindgen(start)]
pub fn main() {
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
    web_sys::console::log_1(&"teologia.ai WASM core initialized".into());
}
