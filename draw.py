from PIL import Image, ImageDraw, ImageFont


def draw_state(maze, visited, dist, backtrack, current):
    BLOCK_SIZE = 32

    nrow = len(maze)
    ncol = len(maze[0])

    img = Image.new('RGB', ((ncol + 2) * BLOCK_SIZE, (nrow + 2) * BLOCK_SIZE),
                    "#2B95C5")

    font = ImageFont.truetype("LiberationMono-Regular.ttf", 24)

    draw = ImageDraw.Draw(img)

    # draw blocks and find start end

    for x in range(ncol):
        for y in range(nrow):
            a = x + 1
            b = y + 1

            if maze[y][x] == '#':
                color = "#2B95C5"
            else:
                if not visited[y][x]:
                    color = "#DCEAF1"
                else:
                    color = "#7E7E7E"

            if maze[y][x].upper() == 'S':
                start = (a * BLOCK_SIZE, b * BLOCK_SIZE)
            if maze[y][x].upper() == 'F':
                finish = (a * BLOCK_SIZE, b * BLOCK_SIZE)

            draw.rectangle([a * BLOCK_SIZE, b * BLOCK_SIZE, (a + 1) *
                            BLOCK_SIZE, (b + 1) * BLOCK_SIZE], color)

    # draw current
    if current is not None:
        a = current[1] + 1
        b = current[0] + 1
        draw.rectangle([a * BLOCK_SIZE, b * BLOCK_SIZE, (a + 1) *
                        BLOCK_SIZE, (b + 1) * BLOCK_SIZE], "#FF935B")

    # draw backtrack
    for c in backtrack:
        a = c[1] + 1
        b = c[0] + 1
        draw.rectangle([a * BLOCK_SIZE, b * BLOCK_SIZE, (a + 1) *
                        BLOCK_SIZE, (b + 1) * BLOCK_SIZE], "#CA4701")

    # draw lines
    for x in range(ncol + 1):
        for y in range(nrow + 1):
            a = x + 1
            b = y + 1
            p1 = [(a * BLOCK_SIZE, 0), (a * BLOCK_SIZE, img.height)]
            p2 = [(0, b * BLOCK_SIZE), (img.width, b * BLOCK_SIZE)]
            draw.line(p1, "#115D81", 2)
            draw.line(p2, "#115D81", 2)

    # draw finish and start text
    width = draw.textsize("S", font)
    start = (start[0] - width[0] / 2 + BLOCK_SIZE / 2,
             start[1] - width[1] / 2 + BLOCK_SIZE / 2)
    finish = (finish[0] - width[0] / 2 + BLOCK_SIZE / 2,
              finish[1] - width[1] / 2 + BLOCK_SIZE / 2)
    draw.text(start, "S", "#115D81", font)
    draw.text(finish, "F", "#115D81", font)

    del draw

    return img
