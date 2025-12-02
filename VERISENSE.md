# Verisense Integration 🦀

This project includes a [Verisense](https://verisense.network) Nucleus to enable decentralized agent capabilities.

## Structure

The Verisense agent is located in `verisense_agent/`. It is a Rust project compiled to WebAssembly.

## Prerequisites

- Rust (latest stable)
- `wasm32-unknown-unknown` target

```bash
rustup target add wasm32-unknown-unknown
```

## Building the Nucleus

To compile the Nucleus to WebAssembly:

```bash
cd verisense_agent
cargo build --release --target wasm32-unknown-unknown
```

The output file will be at `target/wasm32-unknown-unknown/release/verisense_agent.wasm`.

## Functionality

The current Nucleus implements a simple User management system as a proof of concept:
- `add_user(user: User)`: Adds a user to the decentralized storage.
- `get_user(id: u64)`: Retrieves a user by ID.

## Future Plans

- Move Campaign Manager logic to the Nucleus for true autonomy.
- Use Verisense for secure transaction signing and cross-chain coordination.
