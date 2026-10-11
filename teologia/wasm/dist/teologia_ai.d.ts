/* tslint:disable */
/* eslint-disable */

/**
 * Build the æqr badge payload for an artifact id.
 */
export function get_aqr_payload(id: string): string;

/**
 * Get all artifacts as a JSON string.
 */
export function get_artifacts_json(): string;

/**
 * Get platform state as a JSON string.
 */
export function get_platform_state_json(): string;

/**
 * Platform version string.
 */
export function platform_version(): string;

/**
 * Compute the SHA-256 of a byte slice and return it as a lowercase hex string.
 */
export function sha256_hex(data: Uint8Array): string;

/**
 * Verify an artifact by id — returns its metadata as JSON, or an empty string.
 */
export function verify_artifact(id: string): string;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly get_aqr_payload: (a: number, b: number, c: number) => void;
    readonly get_artifacts_json: (a: number) => void;
    readonly get_platform_state_json: (a: number) => void;
    readonly platform_version: (a: number) => void;
    readonly sha256_hex: (a: number, b: number, c: number) => void;
    readonly verify_artifact: (a: number, b: number, c: number) => void;
    readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
    readonly __wbindgen_export: (a: number, b: number) => number;
    readonly __wbindgen_export2: (a: number, b: number, c: number, d: number) => number;
    readonly __wbindgen_export3: (a: number, b: number, c: number) => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
