import plotly.express as px
import os
from .plotcore import load, build_df

def plot(df, color = 'w'):
    range_color = (df[color].min(), df[color].max())
    range_x = (df['x1'].min(), df['x1'].max())
    range_y = (df['x2'].min(), df['x2'].max())
    range_z = (df['x3'].min(), df['x3'].max())
    fig = px.scatter_3d(df, x='x1', y='x2', z='x3', animation_frame='t',
                        color=color, range_x=range_x, range_y=range_y, range_z=range_z, range_color=range_color)

    def fun(scene):
        scene.aspectmode = 'data'
        return
    fig.for_each_scene(fun)
    return fig


def save(fig, fname):
    
    fig.write_html(os.path.join('animations', os.path.basename(fname)).replace('.pkl','.html'), include_plotlyjs='directory',
                   full_html=False, animation_opts={'frame': {'duration': 50}})


if __name__ == '__main__':
    fname = input('Enter data filename (default: most recent): ') or 'most recent'
    color = input('color by? (default: w) ') or 'w'
    data, kwargs, fname = load(fname)
    df, _, kwargs = build_df(data, kwargs)
    fig = plot(df, color=color)
    save(fig, fname)
