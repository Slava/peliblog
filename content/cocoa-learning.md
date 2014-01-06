Title: Cocoa learning
Slug: cocoa-learning
Date: 2013-01-15

Recently I started learning Objective-C and Cocoa framework. I thought it would be easy as I already have some experience with C# and Java. But it appears to be not that easy. Here are some notes I took to map Objective-C to C#.

### Objective-C
- Weakly typed
- Object oriented
- Has manual memory management (Arc)
- Uses LLVM or GCC compiler
- Using LLVM we can combine C, C++, Objective-C code in one file

### Cocoa
Three main frameworks:

- Foundation (Strings, Dates, etc)
- AppKit (UI related framework)
- Core Data (persistence framework)

### Naming conventions
- `NSObject` class names are capitalized
- `dealloc` method names are started with lowercase
- camelCase for local vars

### Some new info for me

- Instance variables that are pointers to other objects are called outlets. 
- Methods that can be triggered by user interface objects are called actions.
- Single inheritance
- Objective-C keywords are prefixed with `@` sign
- Option+Click on any piece of code shows docs
- `@` sign before string literal means Objective-C string class `NSString`
- NSLog has printf-like syntax, but has different identifiers (`%d`, `%qi` for `long long`, `hi` for `short`, etc)
- In NSLog `%@` accepts object pointer and expands it to string by calling `[obj description]`.
- `NSObject.isEqual:anotherObject` by default compares pointers
- Methods starting with `-` are instance methods, starting with `+` are class methods, or static methods
- ARC - automatic reference count is GC and can be disabled for project for manual memory management
- To get selector for method use macros `@selector(method-name)`.
- Document-based application means application runs several copies of itself per opened file, like text editor. System Preferences, for example, is not a document-based application.

### Some types and constants
- `id` is pointer to any type of object
- `BOOL` is the same as `char` but is used as Boolean
- `YES` is 1, `NO` is 0
- IBOutlet is a macro that avaluates to nothing. Ignore it. (`IBOutlet` is a hint to Interface Builder).
- IBAction is the same as `void`. It also acts as a hint to Interface Builder
- `nil` is the same as NULL. We use `nil` instread of `NULL` for poiners to objects.
- `NSArray` can not have `nil` in it
- `NSArray`, `NSNumber` and `NSString` are immutable

### Manual memory management rules
- If you create an object by using a method whose name starts with `alloc` or `new` or contains `copy`, you have taken ownership of it. (That is, assume that the new object has a retain count of 1 and is not in the `autorelease pool`.) You have a responsibility to release the object when you no longer need it. Some of the common methods that convey ownership are `alloc` (which is always followed by an `init` method), `copy`, and `mutableCopy`.
- An object created through any other means, such as a convenience method, is not owned by you. (That is, assume that it has a retain count of 1 and is already in the autorelease pool and thus doomed unless it is retained before the autorelease pool is drained.)
- If you don’t own an object and want to ensure its continued existence, take ownership by sending it the message retain. (This increments the retain count.)
- When you own an object and no longer need it, send it the message `release` or `autorelease`. (The message release decrements the retain count immediately; autorelease causes the message release to get sent when the `autorelease pool` is drained.)
- As long as it has at least one owner, an object will continue to exist- (When its retain count goes to zero, it is sent the message `dealloc`.)

### Controls
#### `NSButton`
Can be oval, square, checkbox. Most common messages sent to buttons:

```objectivec
- (void)setEnabled:(BOOL)yn
- (NSInteger)state
- (void)setState:(NSInteger)aState
```

#### `NSSlider`
Used to select values in ranges. Can be vertical, horizontal and circular. Can send messages continiously while dragging and can send once on mouse button release. Can have markers and prevent selecting values between markers. Two most used messages:

```objectivec
- (void)setFloatValue:(float)x
- (float)floatValue
```

#### `NSField`
Single line input field. Uneditable fields are used as labels.  `NSSecureTextField` is subclass which is used for passwords. 

```objectivec
- (NSString *)stringValue
- (void)setStringValue:(NSString *)aString
- (NSObject *)objectValue
- (void)setObjectValue:(NSObject *)obj
```

Second pair is used in case you use `NSFormatter`s or just `description` method of object.

### temp
- You can programmatically set actions to methods:

	```objectivec
	SEL mySelector;
	mySelector = @selector(drawMickey:);
	[myButton setAction:mySelector];
	```
- For selector at runtime from string use `NSSelectorFromString(@"drawMickey:");`.

### Helper objects
Many classes in the Cocoa framework have an instance variable called `delegate`, you can set the `delegate` outlet to point to a helper object. After some events occur class will refer to helper object. You do not need to implement all helper methods described in documentation. Unimplemented methods will be ignored.

So helper object is object that implements certain protocol (`interface` in Java).
BTW syntax of implementing protocol:

```objectivec
@interface ClassName : ParentClass <Interface1, Interface2, ... > {
	// vars
}

// methods
// properties

@end
```

### Key-Value Coding
Similarly to to JS, we can refer to objects instance property by string key.

```objectivec
@interface Student : NSObject
{
	NSString *firstName;
}
...
@ends
...
Student *s = [[Student alloc] init];
[s setValue:@"Larry" forKey:@"firstName"];
NSString *x = [s valueForKey:@"firstName"];
```

KVC works in pair with binding to GUI, which does not work with direct access to variable. If there are getters and setters for variable, they will be used by methods `setValue:forKey:` and `valueForKey:` only if names of getter and setter satisfy convention `foo` and `setFoo` for property `foo`.

To make other methods affect to bindings, use getters-setters or KVC for changing variable.

### Attributes of property
Syntax for attribute:

```objectivec
@property (attributes) type name;
```

Types of attributes (copy-paste from book):
- `assign` (the default) makes a simple assignment happen. This attribute is most commonly used for scalar, nonpointer types, such as integers and floating-point values.
- `strong` says that this property is a strong reference. It keeps the object being pointed to from being deallocated while this pointer is set. It is specific to ARC code; if you are not using ARC, the retain attribute is equivalent.
- `weak` denotes a weak reference. It is similar to assign, except that once the object being pointed to is deallocated, this property will be set to nil. It is supported only by code compiled with ARC.
- `copy` makes a copy of the new value and assigns the variable to the copy. This attribute is often used for properties that are strings and other classes with mutable subclasses.

There is also `nonatomic` which is self-explanatory, by default getters and setters are atomic.

### Key pathes
If you look better, objects create directed graph. So to any object we can find several pathes, including that starts in itself. You can use it to access variable:

```objectivec
NSString *mn = [selectedPerson valueForKeyPath:@"spouse.scooter.modelName"];
```

You even can use operators in pathes such as `@avg`, `@count`, `@max`, `@min`, `@sum`:

```objectivec
NSNumber *theAverage = [employees valueForKeyPath:@"@avg.expectedRaise"];
```

### Programmatical binding
You can bind programmatically one object to another using pathes:

```objectivec
[textField bind:@"value" toObject:employeeController withKeyPath:@"arrangedObjects.@avg.expectedRaise" options:nil];
```

And unbind:

```objectivec
[textField unbind:@"value"];
```

### Programmatically add observer
Similarly to C#'s `+=` and `-=` event operators(but less functionally reach) you can add observer for value:

```objectivec
[theAppDelegate addObserver:self
	             forKeyPath:@"fido"
	                options:NSKeyValueChangeOldKey
	                context:somePointer];
```

The method that is triggered looks like this:

```objectivec
- (void)observeValueForKeyPath:(NSString *)keyPath
                      ofObject:(id)object
                        change:(NSDictionary *)change
                       context:(void *)context
{
...
}
```

### My mappings for Cocoa objects

- `NSMutableArray <=> vector`
- `NSString <=> string`
- `for (LotteryEntry *entryToPrint in array) <=> foreach`
- `NSAssert <=> assert`
- `interface + implementation <=> class`
- `protocol <=> interface`

