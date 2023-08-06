### Dicy
A simple dice object

#### Features
- Generate as many dice objects as you want
- Each dice object by default allows random.choice
- You can easily iterate on the dice faces

#### Examples

<pre><code>

from dicy import dicy as d
dice_a = d.Dicy()

# this will be evaluated to 1, 2, 3
print(dice_a[0].face)
print(dice_a[1].face)
print(dice_a[2].face)

</code></pre>


