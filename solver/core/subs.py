from .expr import Expression


def subs(expression, old_term, new_term):

    # FIXME: Add type checking
    # TODO: Add multiple subs per call

    final_expression = expression

    if not isinstance(final_expression, Expression):
        if final_expression == old_term:
            return new_term
        else:
            return final_expression

    for i, sub_expression in enumerate(final_expression):

        subs(sub_expression, old_term, new_term)

        if sub_expression == old_term:
            print final_expression.args[i]
            final_expression.args[i] = new_term

    final_expression = final_expression.__class__(*final_expression.args)  # Eval again after substituting

    return final_expression