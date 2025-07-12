import re

def format_recommandation(texte: str) -> str:
    lines = texte.strip().split('\n')
    html_output = []
    in_ul = False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            html_output.append('</ul>')
            in_ul = False

    def replace_link(text):
        return re.sub(r'\[(.*?)\]\((https?://.*?)\)', r'<a href="\2" target="_blank">\1</a>', text)

    for line in lines:
        line = line.strip()

        if line.startswith('### '):  # Titre principal ou complémentaire
            close_ul()
            html_output.append(f'<h3>{line[4:].strip()}</h3>')

        elif line.startswith('- '):  # Élément de liste
            if not in_ul:
                html_output.append('<ul>')
                in_ul = True
            html_output.append(f'<li>{replace_link(line[2:].strip())}</li>')

        elif line.startswith('**') and '**' in line[2:]:  # Ligne en gras
            close_ul()
            bold_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_output.append(f'<p>{replace_link(bold_line)}</p>')

        elif line == '---':
            close_ul()
            html_output.append('<hr>')

        elif line:
            close_ul()
            html_output.append(f'<p>{replace_link(line)}</p>')

    close_ul()
    return '\n'.join(html_output)
