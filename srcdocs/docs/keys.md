<%!
    import mdx_steroids.keys as m
%>
<%
    doc = m.__doc__
%>
# mdx_steroids.keys

!!! note
    This is a fork of [`pymdownx.keys`](http://facelessuser.github.io/pymdown-extensions/extensions/keys/) by Isaac Muse. Please check the [**documentation**](http://facelessuser.github.io/pymdown-extensions/extensions/keys/) on the original author’s site!

${doc}

keystroke | result
-- | --
% for keystroke in m.keymap.keymap:
`${keystroke}` | ++${keystroke}++
% endfor