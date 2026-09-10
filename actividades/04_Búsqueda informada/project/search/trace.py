"""Instrumented ("traced") versions of greedy best-first search and A* for
teaching purposes.

Each `trace_*` function reproduces the exact logic of search/greedy.py and
search/astar.py — same priority-queue frontier, same tie-breaking, same
explored-set handling — but yields a `SearchEvent` at every meaningful step
instead of only returning a final `SearchResult`. Every event carries g(n),
h(n) and, for A*, f(n) = g(n) + h(n), so you can watch exactly why each
algorithm picks the node it picks.

Two ways to watch the trace once you have the events:

- `play_text(events)`          -> step-by-step colored log in the terminal,
                                   with g/h/f shown for every node.
- `animate_graph(events, ...)` -> matplotlib animation of the Romania map.
                                   Every city is permanently labeled with its
                                   h(n) value toward the current goal, and
                                   once the goal is found the path is drawn
                                   in green with g/h/f annotated per city.
                                   (needs `pip install matplotlib`, and
                                   `pip install pillow` to save a .gif)

Run directly for a quick demo:

    python -m search.trace astar --from-city Arad --to Bucharest --mode both
    python -m search.trace greedy --from-city Arad --to Bucharest --mode both
"""

from __future__ import annotations

import argparse
import heapq
import sys
import time
from dataclasses import dataclass, field
from typing import Callable, Iterator

from romania.heuristics import LOCATIONS, heuristic_for
from romania.map import romania_map
from romania.node import Node
from romania.problem import RouteFindingProblem

# --------------------------------------------------------------------------
# Event model
# --------------------------------------------------------------------------

#: start    - the initial node, before anything is expanded
#: pop      - a node is pulled from the priority queue to be expanded
#: generate - a child was generated and pushed onto the frontier
#: prune    - a child (or a stale queue entry) was discarded
#: goal     - the goal test succeeded
#: done     - the search finished without reaching the goal
EventKind = str


@dataclass
class SearchEvent:
    step: int
    kind: EventKind
    state: str | None = None
    frontier: list[str] = field(default_factory=list)
    explored: set[str] = field(default_factory=set)
    g: float | None = None
    h: float | None = None
    f: float | None = None
    depth: int | None = None
    path: list[str] = field(default_factory=list)  # only set on "goal" events
    note: str = ""


# --------------------------------------------------------------------------
# Traced greedy best-first search  (mirrors search/greedy.py)
# --------------------------------------------------------------------------

def trace_greedy(problem: RouteFindingProblem, h: Callable[[str], float]) -> Iterator[SearchEvent]:
    step = 0
    node = Node(problem.start)
    yield SearchEvent(step, "start", node.state, frontier=[node.state], explored=set(), g=node.path_cost, h=h(node.state))

    frontier: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (h(node.state), counter, node))
    frontier_states = {node.state}
    explored: set[str] = set()

    def ordered() -> list[str]:
        return [n.state for _hv, _i, n in sorted(frontier)]

    while frontier:
        _hval, _i, node = heapq.heappop(frontier)
        frontier_states.discard(node.state)
        if node.state in explored:
            step += 1
            yield SearchEvent(step, "prune", node.state, frontier=ordered(), explored=set(explored), note="entrada obsoleta (ya explorado)")
            continue
        if problem.is_goal(node.state):
            step += 1
            yield SearchEvent(
                step, "goal", node.state, frontier=ordered(), explored=set(explored),
                g=node.path_cost, h=h(node.state), depth=node.depth, path=node.path(),
            )
            return

        explored.add(node.state)
        step += 1
        yield SearchEvent(
            step, "pop", node.state, frontier=ordered(), explored=set(explored),
            g=node.path_cost, h=h(node.state), depth=node.depth,
        )

        for child in node.expand(problem):
            s = child.state
            if s in explored or s in frontier_states:
                step += 1
                yield SearchEvent(step, "prune", s, frontier=ordered(), explored=set(explored), note="ya explorado o ya en la frontera")
                continue
            counter += 1
            heapq.heappush(frontier, (h(s), counter, child))
            frontier_states.add(s)
            step += 1
            yield SearchEvent(
                step, "generate", s, frontier=ordered(), explored=set(explored),
                g=child.path_cost, h=h(s), depth=child.depth,
            )

    step += 1
    yield SearchEvent(step, "done", explored=set(explored), note="failure")


# --------------------------------------------------------------------------
# Traced A*  (mirrors search/astar.py)
# --------------------------------------------------------------------------

def trace_astar(problem: RouteFindingProblem, h: Callable[[str], float]) -> Iterator[SearchEvent]:
    step = 0
    node = Node(problem.start)
    yield SearchEvent(
        step, "start", node.state, frontier=[node.state], explored=set(),
        g=node.path_cost, h=h(node.state), f=node.path_cost + h(node.state),
    )

    frontier: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(frontier, (node.path_cost + h(node.state), counter, node))
    best_g = {node.state: 0.0}
    explored: set[str] = set()

    def ordered() -> list[str]:
        return [n.state for _f, _i, n in sorted(frontier)]

    while frontier:
        _f, _i, node = heapq.heappop(frontier)
        if node.state in explored:
            step += 1
            yield SearchEvent(step, "prune", node.state, frontier=ordered(), explored=set(explored), note="entrada obsoleta (ya explorado)")
            continue
        if problem.is_goal(node.state):
            step += 1
            yield SearchEvent(
                step, "goal", node.state, frontier=ordered(), explored=set(explored),
                g=node.path_cost, h=h(node.state), f=node.path_cost + h(node.state),
                depth=node.depth, path=node.path(),
            )
            return

        explored.add(node.state)
        step += 1
        yield SearchEvent(
            step, "pop", node.state, frontier=ordered(), explored=set(explored),
            g=node.path_cost, h=h(node.state), f=node.path_cost + h(node.state), depth=node.depth,
        )

        for child in node.expand(problem):
            s = child.state
            if s in explored:
                step += 1
                yield SearchEvent(step, "prune", s, frontier=ordered(), explored=set(explored), note="ya explorado")
                continue
            if s not in best_g or child.path_cost < best_g[s]:
                best_g[s] = child.path_cost
                counter += 1
                fval = child.path_cost + h(s)
                heapq.heappush(frontier, (fval, counter, child))
                step += 1
                yield SearchEvent(
                    step, "generate", s, frontier=ordered(), explored=set(explored),
                    g=child.path_cost, h=h(s), f=fval, depth=child.depth,
                )
            else:
                step += 1
                yield SearchEvent(step, "prune", s, frontier=ordered(), explored=set(explored), note="g peor que uno ya conocido")

    step += 1
    yield SearchEvent(step, "done", explored=set(explored), note="failure")


# --------------------------------------------------------------------------
# Dispatch
# --------------------------------------------------------------------------

_TRACERS: dict[str, Callable[[RouteFindingProblem, Callable[[str], float]], Iterator[SearchEvent]]] = {
    "greedy": trace_greedy,
    "astar": trace_astar,
}


def run_traced(name: str, problem: RouteFindingProblem, h: Callable[[str], float]) -> Iterator[SearchEvent]:
    if name not in _TRACERS:
        raise ValueError(f"unknown algorithm: {name!r} (choose from {sorted(_TRACERS)})")
    return _TRACERS[name](problem, h)


# --------------------------------------------------------------------------
# Text visualizer
# --------------------------------------------------------------------------

_COLOR = {
    "start": "\033[96m",
    "pop": "\033[93m",
    "generate": "\033[90m",
    "prune": "\033[2m",
    "goal": "\033[92;1m",
    "done": "\033[91;1m",
}
_RESET = "\033[0m"

_LABEL_ES = {
    "start": "INICIO",
    "pop": "EXPANDE",
    "generate": "GENERA",
    "prune": "DESCARTA",
    "goal": "¡META!",
    "done": "FIN",
}


def _ghf(ev: SearchEvent) -> str:
    parts = []
    if ev.g is not None:
        parts.append(f"g={ev.g:.0f}")
    if ev.h is not None:
        parts.append(f"h={ev.h:.0f}")
    if ev.f is not None:
        parts.append(f"f={ev.f:.0f}")
    return " ".join(parts)


def _describe(ev: SearchEvent) -> str:
    stats = _ghf(ev)
    stats_txt = f" ({stats})" if stats else ""
    if ev.kind == "start":
        return f"Comienza en {ev.state}{stats_txt}."
    if ev.kind == "pop":
        return f"Expandiendo {ev.state}{stats_txt}."
    if ev.kind == "generate":
        return f"Se genera {ev.state}{stats_txt}."
    if ev.kind == "prune":
        return f"Se descarta {ev.state}: {ev.note}."
    if ev.kind == "goal":
        return f"Meta encontrada en {ev.state}{stats_txt}."
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
    if use_color is None:
        use_color = sys.stdout.isatty()

    found: SearchEvent | None = None
    for ev in events:
        label = _LABEL_ES.get(ev.kind, ev.kind.upper())
        if use_color:
            color = _COLOR.get(ev.kind, "")
            label = f"{color}{label}{_RESET}"

        frontier_txt = ", ".join(ev.frontier) if ev.frontier else "-"
        print(f"[{ev.step:>3}] {label:<20} {_describe(ev)}")
        print(f"       frontera (ordenada): [{frontier_txt}]")
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
        cost_txt = f"{found.g:.0f} km" if found.g is not None else "?"
        print(f"Profundidad: {found.depth} carreteras   Costo real g(n): {cost_txt}")
    else:
        print("No se encontró un camino a la meta.")


# --------------------------------------------------------------------------
# Graphical visualizer (matplotlib)
# --------------------------------------------------------------------------

def animate_graph(
    events: list[SearchEvent],
    problem: RouteFindingProblem,
    h: Callable[[str], float],
    *,
    title: str = "",
    interval_ms: int = 700,
    save_path: str | None = None,
) -> None:
    """Animates the Romania map using this project's own approximate
    coordinates (romania.heuristics.LOCATIONS).

    Every city is permanently labeled with its h(n) value toward the goal
    of this run. Colors: gris = sin visitar, naranja = en la frontera,
    rojo = siendo expandido ahora, azul = explorado, verde = en el camino
    final. Once the goal is found, the path is drawn in green and every
    city on it is annotated with g / h / f.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.animation import FuncAnimation
    except ImportError as exc:
        raise SystemExit("Este modo necesita matplotlib. Instálalo con: pip install matplotlib") from exc

    graph = problem.graph
    coords = LOCATIONS

    fig, ax = plt.subplots(figsize=(9, 7))
    fig.suptitle(title or "Expansión de nodos")

    for city in graph.cities():
        x1, y1 = coords[city]
        for neighbor, cost in graph.neighbors(city):
            if neighbor < city:
                continue
            x2, y2 = coords[neighbor]
            ax.plot([x1, x2], [y1, y2], color="#cccccc", zorder=1, linewidth=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(cost), fontsize=7, color="#888888")

    (path_line,) = ax.plot([], [], color="#27ae60", linewidth=4, zorder=2.5, solid_capstyle="round")

    scatter = ax.scatter(
        [coords[c][0] for c in graph.cities()],
        [coords[c][1] for c in graph.cities()],
        s=260, zorder=3, color="#bbbbbb", edgecolors="black",
    )
    # Permanent city + h(n) labels (h doesn't change during the search).
    for city in graph.cities():
        x, y = coords[city]
        ax.text(x, y + 14, f"{city}\nh={h(city):.0f}", fontsize=7, ha="center", zorder=4)

    ax.set_axis_off()
    status_text = ax.text(0.01, 0.01, "", transform=ax.transAxes, fontsize=10, va="bottom")

    explored_so_far: set[str] = set()
    frontier_so_far: set[str] = set()
    found_path: list[str] | None = None
    ghf_by_city: dict[str, tuple[float, float, float | None]] = {}

    def color_for(city: str, current: str | None) -> str:
        if found_path is not None and city in found_path:
            return "#2ecc71"
        if city == current:
            return "#e74c3c"
        if city in frontier_so_far:
            return "#f39c12"
        if city in explored_so_far:
            return "#3498db"
        return "#bbbbbb"

    cities = graph.cities()
    hold_frames = 6
    total_frames = len(events) + hold_frames

    def update(frame_idx: int):
        nonlocal explored_so_far, frontier_so_far, found_path
        ev = events[min(frame_idx, len(events) - 1)]
        if frame_idx < len(events):
            explored_so_far = set(ev.explored) if ev.explored else explored_so_far
            frontier_so_far = set(ev.frontier) if ev.frontier else set()
            if ev.state is not None and ev.g is not None:
                ghf_by_city[ev.state] = (ev.g, ev.h, ev.f)
            if ev.kind == "goal" and ev.path:
                found_path = ev.path
        current = ev.state if ev.kind in ("pop", "goal") else None

        scatter.set_color([color_for(c, current) for c in cities])

        if found_path:
            xs = [coords[c][0] for c in found_path]
            ys = [coords[c][1] for c in found_path]
            path_line.set_data(xs, ys)
        else:
            path_line.set_data([], [])

        status_text.set_text(f"paso {ev.step}: {_LABEL_ES.get(ev.kind, ev.kind)} — {ev.note or ev.state or ''}  {_ghf(ev)}")
        return scatter, status_text, path_line

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
    parser = argparse.ArgumentParser(description="Visualiza greedy best-first search y A* paso a paso.")
    parser.add_argument("algorithm", choices=sorted(_TRACERS), help="Algoritmo a trazar")
    parser.add_argument("--from-city", dest="start", default="Arad", help="Ciudad de inicio")
    parser.add_argument("--to", dest="goal", default="Bucharest", help="Ciudad meta")
    parser.add_argument("--mode", choices=["text", "graphic", "both"], default="both")
    parser.add_argument("--delay", type=float, default=0.4, help="Segundos entre eventos en modo texto")
    parser.add_argument("--pause", action="store_true", help="Pausar y esperar Enter en cada paso (modo texto)")
    parser.add_argument("--speed", type=int, default=700, help="Milisegundos entre cuadros en modo gráfico")
    parser.add_argument("--save", default=None, help="Ruta .gif para guardar la animación en vez de mostrarla")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = _build_arg_parser().parse_args(argv)
    problem = RouteFindingProblem(romania_map(), args.start, args.goal)
    h, h_label = heuristic_for(args.goal)
    title = f"{args.algorithm.upper()}: {args.start} → {args.goal} ({h_label})"

    if args.mode in ("text", "both"):
        print(title)
        print("=" * len(title))
        play_text(run_traced(args.algorithm, problem, h), delay=args.delay, pause=args.pause)

    if args.mode in ("graphic", "both"):
        events = list(run_traced(args.algorithm, problem, h))
        animate_graph(events, problem, h, title=title, interval_ms=args.speed, save_path=args.save)


if __name__ == "__main__":
    main()