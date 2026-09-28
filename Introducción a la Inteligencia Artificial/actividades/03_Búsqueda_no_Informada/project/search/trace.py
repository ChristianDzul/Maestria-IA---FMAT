from __future__ import annotations

import argparse
import heapq
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Iterator

from romania.map import romania_map
from romania.node import Node
from romania.problem import RouteFindingProblem


EventKind = str


@dataclass
class SearchEvent:
    step: int
    kind: EventKind
    state: str | None = None
    frontier: list[str] = field(default_factory=list)
    explored: set[str] = field(default_factory=set)
    depth: int | None = None
    cost: float | None = None
    iteration: int | None = None  # only set for ids
    path: list[str] = field(default_factory=list)  # only set on "goal" events
    note: str = ""


# --------------------------------------------------------------------------
# Traced BFS  (mirrors search/bfs.py)
# --------------------------------------------------------------------------

def trace_bfs(problem: RouteFindingProblem) -> Iterator[SearchEvent]:
    step = 0
    node = Node(problem.start)
    yield SearchEvent(step, "start", node.state, frontier=[node.state], explored=set())

    if problem.is_goal(node.state):
        step += 1
        yield SearchEvent(step, "goal", node.state, depth=node.depth, cost=node.path_cost, path=node.path())
        return

    frontier: deque[Node] = deque([node])
    frontier_states = {node.state}
    explored: set[str] = set()

    while frontier:
        node = frontier.popleft()
        frontier_states.remove(node.state)
        explored.add(node.state)
        step += 1
        yield SearchEvent(
            step, "pop", node.state,
            frontier=[n.state for n in frontier], explored=set(explored),
            depth=node.depth, cost=node.path_cost,
        )

        for child in node.expand(problem):
            s = child.state
            if s in explored or s in frontier_states:
                step += 1
                yield SearchEvent(
                    step, "prune", s,
                    frontier=[n.state for n in frontier], explored=set(explored),
                    note="ya explorado o ya en la frontera",
                )
                continue
            if problem.is_goal(s):
                step += 1
                yield SearchEvent(
                    step, "goal", s,
                    frontier=[n.state for n in frontier] + [s], explored=set(explored),
                    depth=child.depth, cost=child.path_cost, path=child.path(),
                )
                return
            frontier.append(child)
            frontier_states.add(s)
            step += 1
            yield SearchEvent(
                step, "generate", s,
                frontier=[n.state for n in frontier], explored=set(explored),
                depth=child.depth, cost=child.path_cost,
            )

    step += 1
    yield SearchEvent(step, "done", explored=set(explored), note="failure")


# --------------------------------------------------------------------------
# Traced DFS  (mirrors search/dfs.py)
# --------------------------------------------------------------------------

def trace_dfs(problem: RouteFindingProblem) -> Iterator[SearchEvent]:
    step = 0
    node = Node(problem.start)
    yield SearchEvent(step, "start", node.state, frontier=[node.state], explored=set())

    if problem.is_goal(node.state):
        step += 1
        yield SearchEvent(step, "goal", node.state, depth=node.depth, cost=node.path_cost, path=node.path())
        return

    frontier: list[Node] = [node]
    frontier_states = {node.state}
    explored: set[str] = set()

    while frontier:
        node = frontier.pop()
        frontier_states.remove(node.state)
        if problem.is_goal(node.state):
            step += 1
            yield SearchEvent(
                step, "goal", node.state,
                frontier=[n.state for n in frontier], explored=set(explored),
                depth=node.depth, cost=node.path_cost, path=node.path(),
            )
            return
        explored.add(node.state)
        step += 1
        yield SearchEvent(
            step, "pop", node.state,
            frontier=[n.state for n in frontier], explored=set(explored),
            depth=node.depth, cost=node.path_cost,
        )

        children = node.expand(problem)
        for child in reversed(children):
            s = child.state
            if s in explored or s in frontier_states:
                step += 1
                yield SearchEvent(
                    step, "prune", s,
                    frontier=[n.state for n in frontier], explored=set(explored),
                    note="ya explorado o ya en la frontera",
                )
                continue
            frontier.append(child)
            frontier_states.add(s)
            step += 1
            yield SearchEvent(
                step, "generate", s,
                frontier=[n.state for n in frontier], explored=set(explored),
                depth=child.depth, cost=child.path_cost,
            )

    step += 1
    yield SearchEvent(step, "done", explored=set(explored), note="failure")


# --------------------------------------------------------------------------
# Traced UCS  (mirrors search/ucs.py)
# --------------------------------------------------------------------------

def trace_ucs(problem: RouteFindingProblem) -> Iterator[SearchEvent]:
    step = 0
    node = Node(problem.start)
    yield SearchEvent(step, "start", node.state, frontier=[node.state], explored=set())

    frontier: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (node.path_cost, counter, node))
    best_cost = {node.state: 0.0}
    explored: set[str] = set()

    def frontier_states_ordered() -> list[str]:
        return [n.state for _c, _i, n in sorted(frontier)]

    while frontier:
        _cost, _i, node = heapq.heappop(frontier)
        if node.state in explored:
            step += 1
            yield SearchEvent(
                step, "prune", node.state,
                frontier=frontier_states_ordered(), explored=set(explored),
                note="entrada obsoleta en la cola (ya explorado)",
            )
            continue
        if problem.is_goal(node.state):
            step += 1
            yield SearchEvent(
                step, "goal", node.state,
                frontier=frontier_states_ordered(), explored=set(explored),
                depth=node.depth, cost=node.path_cost, path=node.path(),
            )
            return

        explored.add(node.state)
        step += 1
        yield SearchEvent(
            step, "pop", node.state,
            frontier=frontier_states_ordered(), explored=set(explored),
            depth=node.depth, cost=node.path_cost,
        )

        for child in node.expand(problem):
            s = child.state
            if s in explored:
                step += 1
                yield SearchEvent(
                    step, "prune", s,
                    frontier=frontier_states_ordered(), explored=set(explored),
                    note="ya explorado",
                )
                continue
            if s not in best_cost or child.path_cost < best_cost[s]:
                best_cost[s] = child.path_cost
                counter += 1
                heapq.heappush(frontier, (child.path_cost, counter, child))
                step += 1
                yield SearchEvent(
                    step, "generate", s,
                    frontier=frontier_states_ordered(), explored=set(explored),
                    depth=child.depth, cost=child.path_cost,
                    note=f"mejor costo conocido: {child.path_cost:.0f} km",
                )
            else:
                step += 1
                yield SearchEvent(
                    step, "prune", s,
                    frontier=frontier_states_ordered(), explored=set(explored),
                    note="costo peor que uno ya conocido",
                )

    step += 1
    yield SearchEvent(step, "done", explored=set(explored), note="failure")


# --------------------------------------------------------------------------
# Traced DLS  (mirrors search/dls.py) — the "frontier" here is the current
# recursion stack (the path from the root to where we currently stand).
# --------------------------------------------------------------------------

def trace_dls(problem: RouteFindingProblem, limit: int) -> Iterator[SearchEvent]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    counter = {"step": 0}
    node = Node(problem.start)
    yield SearchEvent(counter["step"], "start", node.state, frontier=[node.state], explored=set())
    outcome = yield from _trace_recursive_dls(node, problem, limit, counter, stack=[node.state])
    counter["step"] += 1
    if outcome == "goal":
        return
    note = "cutoff" if outcome == "cutoff" else "failure"
    yield SearchEvent(counter["step"], "done", note=note)


def _trace_recursive_dls(
    node: Node,
    problem: RouteFindingProblem,
    limit: int,
    counter: dict[str, int],
    stack: list[str],
) -> Iterator[SearchEvent]:
    """Yields events; returns "goal" | "cutoff" | "failure" via StopIteration value."""
    if problem.is_goal(node.state):
        counter["step"] += 1
        yield SearchEvent(
            counter["step"], "goal", node.state, frontier=list(stack),
            depth=node.depth, cost=node.path_cost, path=node.path(),
        )
        return "goal"
    if limit == 0:
        counter["step"] += 1
        yield SearchEvent(counter["step"], "cutoff", node.state, frontier=list(stack), note="límite de profundidad alcanzado")
        return "cutoff"

    counter["step"] += 1
    yield SearchEvent(counter["step"], "pop", node.state, frontier=list(stack), depth=node.depth, cost=node.path_cost)

    on_path = node.path_states()
    cutoff_occurred = False
    for child in node.expand(problem):
        if child.state in on_path:
            counter["step"] += 1
            yield SearchEvent(
                counter["step"], "prune", child.state, frontier=list(stack),
                note="ya está en el camino actual (evita ciclo)",
            )
            continue
        stack.append(child.state)
        counter["step"] += 1
        yield SearchEvent(counter["step"], "generate", child.state, frontier=list(stack), depth=child.depth, cost=child.path_cost)

        result = yield from _trace_recursive_dls(child, problem, limit - 1, counter, stack)
        stack.pop()
        counter["step"] += 1
        yield SearchEvent(counter["step"], "backtrack", child.state, frontier=list(stack), note=f"resultado de la rama: {result}")

        if result == "cutoff":
            cutoff_occurred = True
        elif result == "goal":
            return "goal"

    return "cutoff" if cutoff_occurred else "failure"


# --------------------------------------------------------------------------
# Traced IDS  (mirrors search/ids.py) — repeats trace_dls with growing limits.
# --------------------------------------------------------------------------

def trace_ids(problem: RouteFindingProblem, max_limit: int | None = None) -> Iterator[SearchEvent]:
    cap = max_limit if max_limit is not None else len(problem.graph.cities())
    step = 0
    for limit in range(0, cap + 1):
        yield SearchEvent(step, "start", problem.start, note=f"nueva iteración con limit={limit}", iteration=limit)
        found_goal = False
        for ev in trace_dls(problem, limit):
            step += 1
            ev.step = step
            ev.iteration = limit
            yield ev
            if ev.kind == "goal":
                found_goal = True
        if found_goal:
            return
    step += 1
    yield SearchEvent(step, "done", note="failure (max_limit alcanzado)")


# --------------------------------------------------------------------------
# Dispatch
# --------------------------------------------------------------------------

_TRACERS = {
    "bfs": lambda problem, limit: trace_bfs(problem),
    "dfs": lambda problem, limit: trace_dfs(problem),
    "ucs": lambda problem, limit: trace_ucs(problem),
    "dls": lambda problem, limit: trace_dls(problem, limit if limit is not None else 3),
    "ids": lambda problem, limit: trace_ids(problem, limit),
}


def run_traced(name: str, problem: RouteFindingProblem, limit: int | None = None) -> Iterator[SearchEvent]:
    if name not in _TRACERS:
        raise ValueError(f"unknown algorithm: {name!r} (choose from {sorted(_TRACERS)})")
    return _TRACERS[name](problem, limit)


# --------------------------------------------------------------------------
# Text visualizer
# --------------------------------------------------------------------------

_COLOR = {
    "start": "\033[96m",       # cyan
    "pop": "\033[93m",         # yellow
    "generate": "\033[90m",    # gray
    "prune": "\033[2m",        # dim
    "goal": "\033[92;1m",      # bold green
    "backtrack": "\033[95m",   # magenta
    "cutoff": "\033[91m",      # red
    "done": "\033[91;1m",      # bold red
}
_RESET = "\033[0m"

_LABEL_ES = {
    "start": "INICIO",
    "pop": "EXPANDE",
    "generate": "GENERA",
    "prune": "DESCARTA",
    "goal": "¡META!",
    "backtrack": "RETROCEDE",
    "cutoff": "CORTE",
    "done": "FIN",
}


def _describe(ev: SearchEvent) -> str:
    if ev.kind == "start":
        return f"Comienza en {ev.state}."
    if ev.kind == "pop":
        cost = f", costo acumulado {ev.cost:.0f} km" if ev.cost is not None else ""
        return f"Expandiendo {ev.state} (profundidad {ev.depth}{cost})."
    if ev.kind == "generate":
        cost = f", costo {ev.cost:.0f} km" if ev.cost is not None else ""
        return f"Se genera {ev.state}{cost}."
    if ev.kind == "prune":
        return f"Se descarta {ev.state}: {ev.note}."
    if ev.kind == "goal":
        cost = f" — costo total {ev.cost:.0f} km" if ev.cost is not None else ""
        return f"Meta encontrada en {ev.state}{cost}."
    if ev.kind == "backtrack":
        return f"Se retrocede desde {ev.state} ({ev.note})."
    if ev.kind == "cutoff":
        return f"Corte por límite de profundidad en {ev.state}."
    if ev.kind == "done":
        return f"Búsqueda terminada: {ev.note}."
    return ev.note


def play_text(
    events: Iterator[SearchEvent],
    *,
    delay: float = 0.0,
    pause: bool = False,
    use_color: bool | None = None,
) -> None:
    """Prints each SearchEvent as a readable, optionally colored, log line.

    delay: seconds to sleep between events (0 = no animation, just fast dump).
    pause: if True, waits for Enter after each event instead of using delay.
    """
    if use_color is None:
        use_color = sys.stdout.isatty()

    last_iteration = None
    found: SearchEvent | None = None
    for ev in events:
        if ev.iteration is not None and ev.iteration != last_iteration:
            last_iteration = ev.iteration
            print(f"\n--- Iteración con límite de profundidad = {ev.iteration} ---")

        label = _LABEL_ES.get(ev.kind, ev.kind.upper())
        if use_color:
            color = _COLOR.get(ev.kind, "")
            label = f"{color}{label}{_RESET}"

        frontier_txt = ", ".join(ev.frontier) if ev.frontier else "-"
        line = f"[{ev.step:>3}] {label:<20} {_describe(ev)}"
        print(line)
        print(f"       frontera: [{frontier_txt}]")
        if ev.explored:
            print(f"       explorados: {{{', '.join(sorted(ev.explored))}}}")

        if ev.kind == "goal" and ev.path:
            print(f"       camino: {' → '.join(ev.path)}")
            found = ev

        if pause:
            input("       (Enter para continuar) ")
        elif delay:
            time.sleep(delay)

    print("\n=== Resumen ===")
    if found is not None:
        print(f"Camino encontrado: {' → '.join(found.path)}")
        print(f"Profundidad: {found.depth} carreteras   Costo: {found.cost:.0f} km")
    else:
        print("No se encontró un camino a la meta.")


# --------------------------------------------------------------------------
# Graphical visualizer (matplotlib)
# --------------------------------------------------------------------------

# Approximate real-world positions (longitude, latitude) for the 20 cities
# in the Romania map — good enough to reproduce the familiar west→east
# layout of the country; not surveyed coordinates.
ROMANIA_COORDS: dict[str, tuple[float, float]] = {
    "Arad": (21.31, 46.18),
    "Bucharest": (26.10, 44.43),
    "Craiova": (23.80, 44.32),
    "Drobeta": (22.66, 44.63),
    "Eforie": (28.63, 44.06),
    "Fagaras": (24.97, 45.84),
    "Giurgiu": (25.97, 43.90),
    "Hirsova": (27.95, 44.69),
    "Iasi": (27.59, 47.16),
    "Lugoj": (21.90, 45.69),
    "Mehadia": (22.36, 44.90),
    "Neamt": (26.38, 46.98),
    "Oradea": (21.92, 47.05),
    "Pitesti": (24.87, 44.86),
    "Rimnicu Vilcea": (24.37, 45.10),
    "Sibiu": (24.15, 45.80),
    "Timisoara": (21.23, 45.75),
    "Urziceni": (26.64, 44.72),
    "Vaslui": (27.73, 46.64),
    "Zerind": (21.52, 46.62),
}


def animate_graph(
    events: list[SearchEvent],
    problem: RouteFindingProblem,
    *,
    title: str = "",
    interval_ms: int = 700,
    save_path: str | None = None,
) -> None:
    """Animates the Romania map, coloring cities as the search progresses.

    Colors: gray = sin visitar, naranja = en la frontera / en el camino
    actual, azul = explorado, rojo = siendo expandido ahora mismo,
    verde = meta encontrada.

    `events` must be a list (not a generator) since it is scanned once to
    build each frame and can be replayed if you call this twice.

    If `save_path` is given (e.g. "bfs.gif"), the animation is saved to
    disk instead of opened in a window (needs `pip install pillow`).
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
    except ImportError as exc:
        raise SystemExit(
            "Este modo necesita matplotlib. Instálalo con: pip install matplotlib"
        ) from exc

    graph = problem.graph
    coords = ROMANIA_COORDS

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.suptitle(title or "Expansión de nodos")

    # Draw static edges once.
    for city in graph.cities():
        x1, y1 = coords[city]
        for neighbor, cost in graph.neighbors(city):
            if neighbor < city:
                continue  # draw each undirected edge once
            x2, y2 = coords[neighbor]
            ax.plot([x1, x2], [y1, y2], color="#cccccc", zorder=1, linewidth=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(cost), fontsize=7, color="#888888")

    # Overlay line for the final path, drawn on top once the goal is found.
    (path_line,) = ax.plot([], [], color="#27ae60", linewidth=4, zorder=2.5, solid_capstyle="round")

    scatter = ax.scatter(
        [coords[c][0] for c in graph.cities()],
        [coords[c][1] for c in graph.cities()],
        s=260, zorder=3, color="#bbbbbb", edgecolors="black",
    )
    for city in graph.cities():
        x, y = coords[city]
        ax.text(x, y + 0.15, city, fontsize=8, ha="center", zorder=4)

    ax.set_axis_off()
    status_text = ax.text(0.01, 0.01, "", transform=ax.transAxes, fontsize=10, va="bottom")
    path_text = ax.text(0.01, 0.97, "", transform=ax.transAxes, fontsize=10, va="top", color="#1e8449", weight="bold")

    explored_so_far: set[str] = set()
    frontier_so_far: set[str] = set()
    found_path: list[str] | None = None

    def color_for(city: str, current: str | None) -> str:
        if found_path is not None and city in found_path:
            return "#2ecc71"       # green — on the found path
        if city == current:
            return "#e74c3c"       # red — being expanded right now
        if city in frontier_so_far:
            return "#f39c12"       # orange — frontier / current path
        if city in explored_so_far:
            return "#3498db"       # blue — explored
        return "#bbbbbb"           # gray — untouched

    cities = graph.cities()
    # Repeat the final event a few extra frames so the highlighted path
    # stays on screen for a moment instead of vanishing instantly.
    hold_frames = 6
    total_frames = len(events) + hold_frames

    def update(frame_idx: int):
        nonlocal explored_so_far, frontier_so_far, found_path
        ev = events[min(frame_idx, len(events) - 1)]
        if frame_idx < len(events):
            explored_so_far = set(ev.explored) if ev.explored else explored_so_far
            frontier_so_far = set(ev.frontier) if ev.frontier else set()
            if ev.kind == "goal" and ev.path:
                found_path = ev.path
        current = ev.state if ev.kind in ("pop", "goal") else None

        colors = [color_for(c, current) for c in cities]
        scatter.set_color(colors)

        if found_path:
            xs = [coords[c][0] for c in found_path]
            ys = [coords[c][1] for c in found_path]
            path_line.set_data(xs, ys)
            path_text.set_text("Camino encontrado: " + " → ".join(found_path))
        else:
            path_line.set_data([], [])
            path_text.set_text("")

        status_text.set_text(f"paso {ev.step}: {_LABEL_ES.get(ev.kind, ev.kind)} — {ev.note or ev.state or ''}")
        return scatter, status_text, path_line, path_text

    anim = FuncAnimation(fig, update, frames=total_frames, interval=interval_ms, repeat=False)

    if save_path:
        anim.save(save_path, writer="pillow")
        print(f"Animación guardada en {save_path}")
    else:
        plt.show()


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Visualiza paso a paso cómo un algoritmo de búsqueda expande nodos."
    )
    parser.add_argument("algorithm", choices=sorted(_TRACERS), help="Algoritmo a trazar")
    parser.add_argument("--from-city", dest="start", default="Arad", help="Ciudad de inicio")
    parser.add_argument("--to", dest="goal", default="Bucharest", help="Ciudad meta")
    parser.add_argument("--limit", type=int, default=None, help="Límite de profundidad (dls) o máximo (ids)")
    parser.add_argument("--mode", choices=["text", "graphic", "both"], default="both")
    parser.add_argument("--delay", type=float, default=0.4, help="Segundos entre eventos en modo texto")
    parser.add_argument("--pause", action="store_true", help="Pausar y esperar Enter en cada paso (modo texto)")
    parser.add_argument("--speed", type=int, default=700, help="Milisegundos entre cuadros en modo gráfico")
    parser.add_argument("--save", default=None, help="Ruta .gif para guardar la animación en vez de mostrarla")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = _build_arg_parser().parse_args(argv)
    problem = RouteFindingProblem(romania_map(), args.start, args.goal)
    title = f"{args.algorithm.upper()}: {args.start} → {args.goal}"

    if args.mode in ("text", "both"):
        print(title)
        print("=" * len(title))
        play_text(
            run_traced(args.algorithm, problem, args.limit),
            delay=args.delay,
            pause=args.pause,
        )

    if args.mode in ("graphic", "both"):
        events = list(run_traced(args.algorithm, problem, args.limit))
        animate_graph(events, problem, title=title, interval_ms=args.speed, save_path=args.save)


if __name__ == "__main__":
    main()