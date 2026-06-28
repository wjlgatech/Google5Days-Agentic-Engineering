# M5 for the 🧒 15-year-old Explorer — Ship It Without Breaking It

*Goal: learn the grown-up secret of shipping — a robot bouncer that won't let a broken version
out the door, and a way to make sure the same bug can never sneak back.*

## Plain explanation

Making something cool is the easy part. **Trusting it enough to give it to real people** is the
hard part — pros say it's about 80% of the work! The trick is a **gate**: before any new version
ships, it has to *pass a test* (the M4 evaluator from last module). Fail → blocked. Pass → try it
on a tiny bit of traffic first (a **canary**, like a taste-test). Still good → a *human* says yes.
And the magic move: when something breaks in the real world, you turn that exact break into a new
test, so it can never break the same way again.

## Concrete example

Three versions try to ship: a good one gets **PROMOTED**, a broken one gets **BLOCKED** (it never
reaches users), and a sneaky one that passes the gate but fails the taste-test gets **ROLLED
BACK**. You'll watch all three happen in one run.

## Hands-on exercise

```bash
cd modules/M5-ship-it-without-breaking-it/exercise
python3 deploy_gate.py            # watch PROMOTED / BLOCKED / ROLLED_BACK
python3 deploy_gate.py --selftest # all ✓
```
Look at the last line: a real-world failure gets turned into a test, and now the version that
*used to* pass gets blocked. That's the loop closing — the system got smarter from a failure.

## Real-world use case

This is why your favorite apps update without suddenly breaking. Behind the scenes a gate like
this checks every new version. The teams that skip it ship bugs to millions of people; the teams
that use it sleep fine.

## Failure mode

**Shipping straight to everyone with no gate and no human.** That's how an AI ends up doing
something embarrassing or expensive in front of real users. Always gate, always canary, always
let a human make the final call.

## Measurable output

```bash
python3 deploy_gate.py --selftest   # all ✓ (promoted, blocked, rolled back, evolve catches it)
```
**You win when** every check is ✓ and you can explain why the broken version never reached "prod".

## Next step

- You've now done all 5 days! Try running the whole [loop](../../loop/README.md) on a tiny
  project of your own: idea → build → test → ship.
- Curious how big companies do "canary" rollouts for real? → read the 30-senior version.
