# OneLongCycleLR

This is a simple adaptation from the OneCycleLR of pytorch.optim package.
The default behaviour is to raise a ValueError when the maximum number of steps is reached. This one instead just keeps on returning the last value.

To install it, just use:

    pip install onelongcyclelr

And to use it you need to import it like

    from onelongcyclelr import OneLongCycleLR

The arguments and keywords needed are exactly the same as the official implementation.