from manim import *

class GluedBinaryTreeAnimation(Scene):
    def construct(self):
        # 1. Setup Title
        self.wait(0.5)
        
        # 2. Define coordinates for Tree 1 (Left Side)
        # Root is on the far left; leaves face inward toward the Y-axis
        pos1 = {
            0: np.array([-4.0, 0, 0]),      # Root
            1: np.array([-2.5, 1.5, 0]),    # Internal Node (Top)
            2: np.array([-2.5, -1.5, 0]),   # Internal Node (Bottom)
            3: np.array([-1.0, 2.25, 0]),   # Leaf 1
            4: np.array([-1.0, 0.75, 0]),   # Leaf 2
            5: np.array([-1.0, -0.75, 0]),  # Leaf 3
            6: np.array([-1.0, -2.25, 0])   # Leaf 4
        }
        
        edges1 = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        
        # Color coding: Roots/Internal = Blue, Leaves (End Points) = Orange
        node_colors = [BLUE, BLUE, BLUE, ORANGE, ORANGE, ORANGE, ORANGE]
        
        # Build Tree 1 structural elements
        tree1_edges = VGroup(*[Line(pos1[u], pos1[v], color=GRAY, stroke_width=3) for u, v in edges1])
        tree1_dots = VGroup(*[Dot(pos1[i], color=node_colors[i], radius=0.15) for i in range(7)])
        tree1 = VGroup(tree1_edges, tree1_dots)
        
        # Step 3: Animate creation of the first normal binary tree
        self.play(Create(tree1_edges), run_time=1.5)
        self.play(FadeIn(tree1_dots, scale=0.5), run_time=1)
        self.wait(1)
        
        # Step 4: Copy the tree and mirror it to the right side
        # Scaling by [-1, 1, 1] around the origin perfectly mirrors it horizontally
        tree2 = tree1.copy().scale([-1, 1, 1], about_point=ORIGIN)
        
        self.play(
            TransformFromCopy(tree1, tree2),
            run_time=2
        )
        self.wait(1)
        
        # Step 5: Highlight the end points (Leaves) that will be joined
        # Indices 3, 4, 5, 6 correspond to the leaves in our setup
        flash_animations = [
            Flash(tree1[1][i], color=ORANGE, flash_radius=0.2, num_lines=8) for i in [3, 4, 5, 6]
        ] + [
            Flash(tree2[1][i], color=ORANGE, flash_radius=0.2, num_lines=8) for i in [3, 4, 5, 6]
        ]
        
        self.play(AnimationGroup(*flash_animations, lag_ratio=0.1))
        self.wait(0.5)
        
        # Step 6: Join them by drawing the "gluing" edges
        gluing_edges = VGroup()
        for i in [3, 4, 5, 6]:
            start_pt = tree1[1][i].get_center()
            end_pt = tree2[1][i].get_center()
            # Draw distinct red edges showing the connection/gluing
            edge = Line(start_pt, end_pt, color=RED, stroke_width=4)
            gluing_edges.add(edge)
            
        self.play(Create(gluing_edges), run_time=2, lag_ratio=0.25)
        self.wait(1)
        
        # Final Step: Unified network look
        # Fade the gluing lines to match the rest of the tree structure
        self.play(
            gluing_edges.animate.set_color(GRAY).set_stroke_width(3),
            run_time=1.5
        )
        self.wait(2)