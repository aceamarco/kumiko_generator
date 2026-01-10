import math

from geometry.pattern.pattern import Pattern


class StarPattern(Pattern):
    def generate(self):
        lines = []
        for i in range(3):
            angle = math.radians(i * 60)
            x = math.sin(angle) * 0.9
            y = math.cos(angle) * 0.9
            lines.append(
                f'<line x1="0" y1="0" x2="{x:.3f}" y2="{y:.3f}" stroke="black" stroke-width="0.05" />'
            )
        # Optional: debug canonical triangle outline
        lines.append('<polygon points="0,-1 -0.866,0.5 0.866,0.5" fill="none" stroke="red" stroke-width="0.02" />')
        return "\n".join(lines)

