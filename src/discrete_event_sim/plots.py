def save_fig(
    fig,
    filename,
    output_dir,
    rect=None,
):
    """Function to save figures."""
    fig.tight_layout(rect=rect)
    fig.savefig(output_dir / f"{filename}.png", bbox_inches="tight")
