from magic_regexp import CaracteresEspeciais, ConstrutorRegex, GrupoCaracteres

cr = ConstrutorRegex()


def test_example_DetectScriptTag():
    """
    Reference: https://regexr.com/3h62s
    Regex: <.*script.*/?>
    """
    m_regex = (
        cr.contenha('<')
        .zero_ou_mais(CaracteresEspeciais.QUALQUER)
        .contenha('script')
        .zero_ou_mais(CaracteresEspeciais.QUALQUER)
        .zero_ou_uma('/')
        .contenha('>')
    ).construir()

    assert (
        m_regex.findall(
            """
    <script>
    <script />
    <script></script>
    <script lorem></script>
    <script lorem />
    < script>
    <scriptscriptscript><%adsU&#script>
    lorem lo rem<script>lorem<script>
    <SCRiPT>
    <script lorem lorem> </script>
    <script>alert(\'a\')</script>
    """
        )
        == [
            '<script>',
            '<script />',
            '<script></script>',
            '<script lorem></script>',
            '<script lorem />',
            '< script>',
            '<scriptscriptscript><%adsU&#script>',
            '<script>lorem<script>',
            '<script lorem lorem> </script>',
            "<script>alert('a')</script>",
        ]
    )


def test_example_JavascriptCommentRemoval():
    """
    Reference: https://regexr.com/3aeb7
    Regex: \\/\\*[\\s\\S]*?\\*\\/|\\/\\/.*
    """

    regex = (
        cr.contenha('/')
        .contenha('\\*')
        .zero_ou_mais(
            GrupoCaracteres(
                CaracteresEspeciais.ESPACO_EM_BRANCO,
                CaracteresEspeciais.NAO_ESPACO_EM_BRANCO,
            )
        )
        .contenha('\\*')
        .contenha('/')
        .contenha('|')
        .contenha('/')
        .contenha('/')
        .zero_ou_mais(CaracteresEspeciais.QUALQUER)
    ).construir()

    assert (
        regex.findall(
            """
var sample    = 0;
var new       = 1;
var my_string = \"Hello World!\";

// This is a comment!

function do_stuff(){
	alert(my_string);//another comment
}

/* This is
 * a multiline
 * comment!
 */

var something;

/* programs/applications 16/*(4*2)=2 */

if(sample > new){
  do_stuff(/* arguments here */);
}

//

/**/

        """
        )
        == [
            '// This is a comment!',
            '//another comment',
            '/* This is\n'
            ' * a multiline\n'
            ' * comment!\n'
            ' */\n'
            '\n'
            'var something;\n'
            '\n'
            '/* programs/applications 16/*(4*2)=2 */\n'
            '\n'
            'if(sample > new){\n'
            '  do_stuff(/* arguments here */);\n'
            '}\n'
            '\n'
            '//\n'
            '\n'
            '/**/',
        ]
    )


def test_exemple_CPFBrasil():
    """
    Reference: https://regexr.com/3dhp9
    Regex: [0-9]{3}\\.?[0-9]{3}\\.?[0-9]{3}\\-?[0-9]{2}
    """

    regex = (
        cr.exatamente_n(3, CaracteresEspeciais.DIGITO)
        .zero_ou_uma('\\.')
        .exatamente_n(3, CaracteresEspeciais.DIGITO)
        .zero_ou_uma('\\.')
        .exatamente_n(3, CaracteresEspeciais.DIGITO)
        .zero_ou_uma('-')
        .exatamente_n(2, CaracteresEspeciais.DIGITO)
    ).construir()

    assert (
        regex.findall(
            """
    Com Pontuação:
        000.000.000-00;

    Sem Potuação:
        11111111111;

    Simbolos invalidos:
        222-222-222.22;
        123-456-789-00;
        123X456%789-00;
        123通456💩789-00;
    """
        )
        == ['000.000.000-00', '11111111111']
    )
