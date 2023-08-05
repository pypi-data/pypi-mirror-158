# neural-network-renderer

The code generating the image is writen in Python. This code generates `.tex` and `.sty` files that are directly compiled and deleted once the resulting PDF is available.

## Example

Here is an example of the code to generate a simple convolutionnal-network representation:

```Python
from neural_network_renderer.architecture import Architecture
from neural_network_renderer.colors import Colors
from neural_network_renderer.layers import Conv, ConvConvRelu, Dense, DottedLines, Input, Pool, Softmax, Spacer

def main():
    Colors.Dense("lightgray")
    Colors.Softmax("lightgray")

    arch = Architecture(4 / 32)
    # first layer
    arch.add(ConvConvRelu(s_filter=64, n_filter=[32, 32], to="(5,0,0)"))
    arch.add(Pool([32, 32, 32]))
    arch.add(Spacer(width=20))

    # second layer
    arch.add(ConvConvRelu(s_filter=32, n_filter=[64, 64]))
    arch.add(Pool([16, 16, 64]))

    arch.add(Spacer())

    # third layer
    arch.add(ConvConvRelu(s_filter=16, n_filter=[64, 64]))
    arch.add(Pool([8, 8, 64], name="last_pool"))
    arch.add(Spacer())

    # GPA
    arch.add(Conv(s_filter=8, n_filter=1, name="gpa", caption="GPA"))

    # flatten
    arch.add(Dense(64, name="flatten", offset="(4,0,0)", caption="Hidden Layer"))
    arch.add(Softmax(5, 5, name="output", caption="Output", offset="(4,0,0)"))

    arch.add(DottedLines("gpa", "flatten"))
    arch.add(DottedLines("flatten", "output"))

    arch.to_pdf("output_file")


if __name__ == "__main__":
    main()

```