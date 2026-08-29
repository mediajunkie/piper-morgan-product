# ADR-012: Protocol-Ready JWT Authentication

**Date**: 2025-08-10
**Status**: ACCEPTED
**Context**: Security Sunday Sprint - Protocol-First Foundation

## Context and Problem Statement

Piper Morgan requires a secure, scalable authentication system that enables:
1. **Protocol Portability**: Compatible with MCP (Model Context Protocol) and other AI agent ecosystems
2. **Federation Ready**: Supports cross-system authentication for agent-to-agent communication
3. **Ecosystem Participation**: OAuth 2.0 compliance for third-party integrations
4. **Future-Proof Architecture**: Extensible for protocol evolution and multi-agent workflows

Current session-based authentication limits protocol integration and federation capabilities.

## Decision Drivers

### Strategic Requirements
- **MCP Protocol Integration**: JWT enables stateless authentication across protocol boundaries
- **Agent Federation**: Standard claims structure supports agent-to-agent authentication
- **Ecosystem Hub Vision**: OAuth 2.0 compliance positions Piper as intelligence hub
- **Cross-Platform Portability**: JWTs work across web, API, and protocol interfaces

### Technical Requirements
- **Stateless Operation**: No server-side session storage for protocol compatibility
- **Standard Claims**: RFC 7519 compliance for interoperability
- **Secure Implementation**: Industry-standard security practices
- **Performance**: <10ms token validation for real-time protocol operations

### Business Requirements
- **Market Positioning**: Standards-compliant authentication for enterprise adoption
- **Integration Velocity**: Reduces friction for third-party integrations
- **Scaling Preparation**: Supports multi-tenant and federated deployments

## Considered Options

### Option 1: Session-Based Authentication (Current)
**Pros**: Simple, familiar, good for monolithic applications
**Cons**: Protocol incompatible, federation impossible, scaling limitations

### Option 2: JWT with Custom Claims
**Pros**: Flexible, fast development
**Cons**: Poor interoperability, federation challenges, non-standard

### Option 3: Standards-Compliant JWT (Selected)
**Pros**: Protocol ready, federation enabled, ecosystem compatible
**Cons**: More complex implementation, token management overhead

## Decision Outcome

**Chosen Option**: Standards-Compliant JWT Authentication with Protocol Extensions

### Core Implementation
```python
# JWT Standard Claims (RFC 7519)
{
  "iss": "https://piper-morgan.ai",           # Issuer
  "sub": "user:12345",                        # Subject (User ID)
  "aud": ["piper-api", "mcp-protocol"],       # Audience
  "exp": 1734567890,                          # Expiration
  "iat": 1734564290,                          # Issued At
  "jti": "uuid-token-id"                      # JWT ID
}

# Piper-Specific Claims
{
  "role": "pm",                               # User role
  "permissions": ["projects.read", "..."],    # Fine-grained permissions
  "context_id": "session-uuid",               # Session context
  "protocol_version": "1.0"                   # Protocol compatibility
}
```

### Protocol Integration Strategy
```yaml
MCP Authentication Flow:
  1. Client authenticates via OAuth 2.0 → JWT issued
  2. JWT included in MCP protocol headers
  3. Protocol server validates JWT → grants access
  4. Agent-to-agent calls use JWT delegation

Federation Pattern:
  1. Piper issues JWT with federation claims
  2. Partner systems validate via public key
  3. Cross-system operations use delegated tokens
  4. Audit trail maintained across federation
```

## Consequences

### Positive
- **Protocol Integration**: Seamless MCP and agent protocol support
- **Federation Capability**: Agent-to-agent authentication enabled
- **Ecosystem Readiness**: OAuth 2.0 compliance for enterprise integrations
- **Performance**: Stateless validation <10ms for real-time operations
- **Scalability**: No server-side session storage requirements
- **Security**: Industry-standard token security with rotation

### Negative
- **Complexity**: More sophisticated token management required
- **Token Management**: Refresh token rotation and secure storage needed
- **Key Management**: Public/private key infrastructure required

### Neutral
- **Migration Path**: Gradual transition from session-based authentication
- **Backward Compatibility**: Session authentication maintained during transition

## Implementation Roadmap

### Phase 1: Foundation (Sprint 1)
- JWT service implementation with standard claims
- Public/private key generation and management
- Basic token validation middleware
- User authentication flow with JWT issuance

### Phase 2: Protocol Integration (Sprint 2)
- MCP protocol header authentication
- Agent-to-agent JWT delegation patterns
- Protocol version compatibility handling
- Cross-system validation infrastructure

### Phase 3: Federation (Sprint 3)
- OAuth 2.0 provider implementation
- Third-party system integration patterns
- Federated authentication flows
- Cross-domain trust establishment

### Phase 4: Ecosystem Hub (Future)
- Multi-tenant JWT issuance
- Agent marketplace authentication
- Protocol federation standards participation
- Enterprise SSO integration

## Security Considerations

### Token Security
- **RSA-256 Signatures**: Cryptographically secure token signing
- **Short-Lived Tokens**: 15-minute access tokens with refresh rotation
- **Secure Storage**: HttpOnly cookies for web, secure storage for protocols
- **Token Rotation**: Automatic refresh with blacklist management

### Protocol Security
- **Audience Validation**: Strict audience claims for protocol endpoints
- **Permission Scoping**: Fine-grained permissions for protocol operations
- **Cross-Origin Protection**: CORS policies for web-based protocol access
- **Rate Limiting**: Token-based rate limiting for protocol calls

### Federation Security
- **Key Distribution**: Secure public key distribution for validation
- **Trust Relationships**: Explicit trust establishment with federated systems
- **Audit Logging**: Comprehensive audit trail for federated operations
- **Revocation**: Real-time token revocation across federated systems

## Related ADRs
- **ADR-007**: Unified Session Management Architecture (superseded by JWT)
- **ADR-010**: Configuration Patterns (supports JWT configuration)
- **Future ADR-013**: MCP Protocol Integration Architecture (will build on this JWT foundation)

## References
- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/introduction)
- [OpenID Connect Core Specification](https://openid.net/specs/openid-connect-core-1_0.html)

---

**Strategic Impact**: Protocol-ready authentication foundation enabling MCP integration, agent federation, and ecosystem hub positioning for Piper Morgan's evolution to multi-agent intelligence platform.
