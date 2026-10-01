def make_solver_settings(blocks, abs_tol=1e-10, rel_tol=1e-10):
    """Factory for solver settings dicts. Reduces boilerplate across all figure settings."""
    return {
        'integrator': 'cvode',
        'absolute_tolerance': abs_tol,
        'relative_tolerance': rel_tol,
        'stiff': True,
        'variable_step_size': True,
        'simulation_blocks': blocks,
    }

def solver_settings_Bloomingdale(experiment):
    return make_solver_settings(
        {'block1': {'start': 0, 'end': 1000, 'n_points': 100001, 'abs_tol':1e-14, 'rel_tol':1e-14}}
    )
