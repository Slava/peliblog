Title: Good grid view for Cocoa app
Slug: good-grid-view-for-cocoa-app
Date: 2013-03-19

There are different styles of presenting data but there is one that is used whenever you need to present lots of data and each piece has its own visual representation. I am talking about grid with big icons representing the data. Sometimes working on Cocoa application, built-in `IKImageBrowser` does not satisfy our needs. `OEGridView` comes to help.

`OEGridView` is part of [OpenEmu][OpenEmuWebsite] project which is awesome by itself. There are a lot of things you can learn just reading [code of the project][OpenEmuGithub]. Grid view representing collections of games with cool covers is one of them.

Similary to `IKImageBrowser` custom grid is based on layers. There is a sublayer of main layer for each cell. Layers are chosen over views due to performance reasons. Another optimization is reusing all cells, which are not visible at the moment.

`OEGridView` has two protocols as any other Cocoa control: delegate and data source.

Data source is identical to `NSTableView` with slightly changed API. Same situation is with delegate by the way.

The only worry is custom `OEGridViewCell` subclass, which is subclass of `CALayer`. Visual representation can be achieved with bunch of sublayers arranged in correct order.

Issue you can meet after implementing fency cell layer: renaming of title in `OEGridView` is hoping that title is actually a subclass of `CATextLayer` and is easily accessible with mouse double click. So placing title layer in unusual place can block the renaming feature.

Another issue I ran into was the fact that grid view reuses cell instances. `- (OEGridViewCell *)gridView:cellForItemAtIndex:` should be implemented in the way similar to this:

```objectivec
- (OEGridViewCell *)gridView:(OEGridView *)gridView cellForItemAtIndex:(NSUInteger)index
{
    // Maybe cell on such position already exists?
    MYCustomGridViewCell *item = (MYCustomGridViewCell *)[gridView cellForItemAtIndex:index makeIfNecessary:NO];

    // If not, maybe there are cell instance we can reuse
    if (!item)
        item = (MYCustomGridViewCell *)[gridView dequeueReusableCell];
        
    // OK, create new one
    if (!item)
        item = [[MYCustomGridViewCell alloc] init];
        
    // Set the binding
    id object = [self.contents objectAtIndex:index];
    item.objectBinding = object;

    return item;
}
```

So you reuse maximum of cells you can. And do not forget to override the `- (void)prepareForReuse` method. The issue I had with this method was quite funny. In this preparation method I was preparing the cell in very hard way: clearing all layers and properties. But did not update the layers if the new binding object was the same object it was binded to before.

[Indragiek][indragiek] has done a great job and extracted `OEGridView` classes. Check out [the repo on github][OEGridViewRepo].

[OpenEmuWebsite]: http://openemu.org/
[OpenEmuGithub]: https://github.com/OpenEmu/OpenEmu
[indragiek]: https://github.com/indragiek
[OEGridViewRepo]: https://github.com/indragiek/OEGridView