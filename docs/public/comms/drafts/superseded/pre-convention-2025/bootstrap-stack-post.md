# The $0 Bootstrap Stack: Building Enterprise Infrastructure for Free (With Upgrade Paths)

*Building Piper Morgan, Part 7 • July 8, 2025*

After deciding to rebuild Piper Morgan from scratch, I faced a classic dilemma: How do you build enterprise-grade infrastructure when your budget is exactly zero dollars?

The answer turned out to be a 300-line bash script and some strategic thinking about the future.

## The Price of "Enterprise"

Let me paint you a picture. A typical "enterprise" PM platform might run:
- Auth0: $240/month
- Datadog: $75/month after free tier
- Pinecone: $70/month after free tier
- Various other services: $200+/month

Total: $500-600/month before you've written a line of business logic.

For a side project? That's a non-starter. But here's what I learned at [ADD PERSONAL ANECDOTE FROM 18F ABOUT GOVERNMENT BUDGETS AND CONSTRAINTS]: sometimes constraints force better decisions.

## The Philosophy

The key insight wasn't to find free alternatives to enterprise tools. It was to find free tools that could *become* enterprise tools. Every component needed a clear upgrade path.

Here's what that looked like:
- Keycloak (free) → Auth0 ($240/month) when ready
- ChromaDB (free) → Pinecone ($70/month) for scale
- Prometheus/Grafana (free) → Datadog ($75/month) for convenience

The migration path was built in from day one. No vendor lock-in, just vendor... pre-selection?

## The Bootstrap Script

What emerged was a massive bash script that would set up everything:

```bash
#!/bin/bash
# bootstrap-stack.sh - Complete setup for $0 budget Piper Morgan infrastructure

echo "🚀 Setting up Piper Morgan Bootstrap Stack..."
```

This script created:
- PostgreSQL for core data
- Redis for caching and queues
- Keycloak for authentication
- ChromaDB for vector storage
- Temporal for workflow orchestration
- Prometheus/Grafana for monitoring
- Traefik as API gateway

All running in Docker. All configured and ready. All free.

## The Comedy Continues

Of course, nothing ever works on the first try. Remember those Python environment issues from the last post? They had friends.

```bash
docker info
Cannot connect to the Docker daemon at unix:///Users/xian/.docker/run/docker.sock
```

Docker wasn't running. Such a simple thing, but there I was, troubleshooting connection errors when the real problem was I forgot to start Docker Desktop. It's always the simple things that get you.

Then came the environment variables. You know that feeling when you realize you've been debugging the wrong thing for an hour? That was me discovering my `.env` file wasn't being loaded because I was in the wrong directory.

[SPECIFIC EXAMPLE NEEDED: A funny misconfiguration or typo from the actual setup]

## What This Stack Actually Does

Beyond saving $600/month, this bootstrap approach provided:

1. **Complete isolation**: Everything runs in containers
2. **One-command setup**: New developers can be up in minutes
3. **Production parity**: The same stack works locally and in production
4. **Monitoring from day one**: Not an afterthought

The monitoring deserves special mention. By starting with Prometheus and Grafana, I had visibility into everything from the beginning. When things broke (and oh, did they break), I could actually see why.

## The Hidden Costs

"Free" doesn't mean "cheap." This approach cost:
- 2 weeks of setup time
- Significant Docker expertise required
- More operational complexity
- No vendor support when things break

But here's the thing: I was going to spend those 2 weeks debugging vendor integrations anyway. At least this way, I understood my entire stack.

[ADD PERSONAL ANECDOTE FROM 7 CUPS/CLOUDON ABOUT BUILD VS BUY DECISIONS]

## The Upgrade Path Magic

The real magic was in the upgrade paths. When you outgrow ChromaDB's free tier, switching to Pinecone is a configuration change, not a code rewrite. When you need Auth0's enterprise features, Keycloak has prepared you for OIDC patterns.

Every "free" choice was actually a "free to start" choice.

## What I Learned

Building on a budget forces architectural discipline. You can't throw money at problems, so you have to actually solve them. You can't rely on vendor magic, so you have to understand your stack.

The bootstrap script became a living document of the infrastructure. Every decision, every configuration, every gotcha—all captured in executable form.

## Still Setting Up

Three days into what I thought would be a few hours of setup, I was still configuring Keycloak realms. My terminal history was a monument to trial and error:

```bash
docker-compose up -d
docker-compose down
docker-compose up -d --force-recreate
docker-compose down -v  # nuclear option
```

But each failure taught me something about the system I was building. By the time everything worked, I understood every component intimately.

[CHRISTIAN TO POLISH: Add current perspective on whether this approach was worth it]

## The Payoff

Six months later (spoiler alert), this infrastructure has scaled to handle real workloads without spending a dollar on infrastructure. The monitoring caught issues before users did. The auth system just worked. The vector database performed better than expected.

Most importantly, when it came time to add that first paid service, the upgrade was seamless. The architecture was ready for it.

Sometimes the best investment is the time you spend not spending money.

---

*Next in Building Piper Morgan: From Task Executor to Strategic Thinking Partner (or, why we burned it all down)*

[CONSIDER CULTURAL REFERENCE HERE: Something about bootstrap pulling, maybe?]
