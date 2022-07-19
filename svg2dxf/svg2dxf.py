import argparse

import ezdxf
import svgpathtools


def main() -> int:
    """main function."""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="svg input file", type=str)
    parser.add_argument(
        "-o", "--output", help="save to dxf file", type=str, default=None
    )
    args = parser.parse_args()

    paths, attributes, svg_attributes = svgpathtools.svg2paths2(args.filename)

    height = 200
    size_attr = svg_attributes.get("-viewBox", "").split()
    if len(size_attr) == 4:
        height = float(size_attr[3])
    else:
        height_attr = svg_attributes.get("height")
        if height_attr.endswith("mm"):
            height = float(height_attr[0:-2])

    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    for path in paths:
        # check if circle
        if (
            len(path) == 2
            and isinstance(path[0], svgpathtools.path.Arc)
            and isinstance(path[1], svgpathtools.path.Arc)
            and path.start == path.end
            and path[0].radius.real == path[0].radius.imag
            and path[1].radius.real == path[1].radius.imag
            and path[0].rotation == 0.0
            and path[1].rotation == 0.0
            and path[0].delta == -180.0
            and path[1].delta == -180.0
        ):
            msp.add_circle(
                (path[0].center.real, height - path[0].center.imag), path[0].radius.real
            )
        else:
            for segment in path:
                if isinstance(segment, svgpathtools.path.Line):
                    msp.add_line(
                        (segment.start.real, height - segment.start.imag),
                        (segment.end.real, height - segment.end.imag),
                    )
                else:
                    last_x = segment.start.real
                    last_y = segment.start.imag
                    nump = int(segment.length() / 3) + 1
                    for n in range(0, nump):
                        p = segment.point(n / nump)
                        msp.add_line(
                            (last_x, height - last_y), (p.real, height - p.imag)
                        )
                        last_x = p.real
                        last_y = p.imag
                    msp.add_line(
                        (last_x, height - last_y),
                        (segment.end.real, height - segment.end.imag),
                    )

    if args.output is None:
        args.output = f"{'.'.join(args.filename.split('.')[0:-1])}.dxf"

    print(f"writing to dxf file: {args.output}")
    for vport in doc.viewports.get_config("*Active"):
        vport.dxf.grid_on = True
        vport.dxf.aspect_ratio = 1
        vport.dxf.height = height
        vport.dxf.center = (height / 2, height / 2)
    doc.saveas(args.output)


if __name__ == "__main__":
    sys.exit(main())
