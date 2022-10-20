from jpype import startJVM, getDefaultJVMPath, JPackage, java


CDK_JARFILE_PATH = "/code/cdk.jar"
OPSIN_JARFILE_PATH = "/code/opsin.jar"
WURCS_JARFILE_PATH = "/code/MolWURCS.jar"

# Start java virtual machine
startJVM(
    getDefaultJVMPath(),
    f"-Djava.class.path={CDK_JARFILE_PATH}:{OPSIN_JARFILE_PATH}:{WURCS_JARFILE_PATH}",
    convertStrings=False,
)


cdk = JPackage("org").openscience.cdk
MDLV2000Reader = cdk.io.MDLV2000Reader
MDLV2000Writer = cdk.io.MDLV2000Writer
MDLV3000Reader = cdk.io.MDLV3000Reader
MDLV3000Writer = cdk.io.MDLV3000Writer
SmilesParser = cdk.smiles.SmilesParser
SmilesGenerator = cdk.smiles.SmilesGenerator
SilentChemObjectBuilder = cdk.silent.SilentChemObjectBuilder
StructureDiagramGenerator = cdk.layout.StructureDiagramGenerator
AtomContainer = cdk.AtomContainer
AtomContainerManipulator = cdk.tools.manipulator.AtomContainerManipulator
MolecularFormulaManipulator = cdk.tools.manipulator.MolecularFormulaManipulator
DepictionGenerator = cdk.depict.DepictionGenerator
Projection = cdk.stereo.Projection
StereoElementFactory = cdk.stereo.StereoElementFactory
StringReader = java.io.StringReader
StringWriter = java.io.StringWriter

opsin = JPackage("uk").ac.cam.ch.wwmm.opsin
NameToStructure = opsin.NameToStructure

glycoinfo = JPackage("org").glycoinfo
MoleculeToWURCSGraph = glycoinfo.MolWURCS.exchange.toWURCS.MoleculeToWURCSGraph
WURCSFactory = glycoinfo.WURCSFramework.util.WURCSFactory
WURCSGraph = glycoinfo.WURCSFramework.wurcs.graph.WURCSGraph


def read_mol(item):
    input_format = None
    if "V2000" in item.structure:
        mr = MDLV2000Reader(StringReader(item.structure))
        mol = mr.read(AtomContainer())
        input_format = "V2000"
    elif "V3000" in item.structure:
        mr = MDLV3000Reader(StringReader(item.structure))
        mol = mr.read(AtomContainer())
        input_format = "V3000"
    else:
        sp = SmilesParser(SilentChemObjectBuilder.getInstance())
        try:
            mol = sp.parseSmiles(item.structure)
            # generate 2D coordinates
            sdg = StructureDiagramGenerator()
            sdg.setMolecule(mol)
            sdg.generateCoordinates()
            mol = sdg.getMolecule()
            input_format = "SMILES"
        except:
            mol = None

    if mol and item.gen_coords:
        # generate 2D coordinates
        sdg = StructureDiagramGenerator()
        sdg.setMolecule(mol)
        sdg.generateCoordinates()
        mol = sdg.getMolecule()
    return mol, input_format


def write_mol(mol, out_format):
    out = None
    if out_format == "V2000":
        out = StringWriter()
        mw = MDLV2000Writer(out)
        mw.write(mol)
    elif out_format == "V3000":
        out = StringWriter()
        mw = MDLV3000Writer(out)
        mw.write(mol)
    elif out_format == "SMILES":
        sg = SmilesGenerator.absolute()
        out = sg.create(mol)
    elif out_format == "WURCS":
        graphs = MoleculeToWURCSGraph().start(mol)
        if graphs:
            factory = WURCSFactory(graphs[0])
            out = factory.getWURCS()
    return out


def convert_mol(item):
    out = None
    mol, _ = read_mol(item)
    if mol:
        out = write_mol(mol, item.out_format)
    return out


def add_stereo_elements(item):
    mol, input_format = read_mol(item)
    if mol:
        mol.setStereoElements(
            StereoElementFactory.using3DCoordinates(mol)
            .interpretProjections(Projection.Chair, Projection.Haworth)
            .createAll()
        )
        out = write_mol(mol, input_format)
    else:
        out = None
    return out


def add_hydrogens(item):
    mol, input_format = read_mol(item)
    if mol:
        AtomContainerManipulator.convertImplicitToExplicitHydrogens(mol)
        out = write_mol(mol, input_format)
    else:
        out = None
    return out


def remove_hydrogens(item):
    mol, input_format = read_mol(item)
    if mol:
        AtomContainerManipulator.suppressHydrogens(mol)
        out = write_mol(mol, input_format)
    else:
        out = None
    return out


def depict_image(item):
    svg = None
    mol, _ = read_mol(item)
    if mol:
        depiction = (
            DepictionGenerator()
            .withSize(item.width, item.heigth)
            .withFillToFit()
            .withAtomColors()
            .depict(mol)
        )
        svg = depiction.toSvgStr()
    return svg


def calculate_formula(item):
    mol_formula = None
    mol, _ = read_mol(item)
    if mol:
        AtomContainerManipulator.convertImplicitToExplicitHydrogens(mol)
        molecularFormula = MolecularFormulaManipulator.getMolecularFormula(mol)
        mol_formula = MolecularFormulaManipulator.getString(molecularFormula)
    return mol_formula


def name_to_structure(name):
    nts = NameToStructure.getInstance()
    try:
        out = nts.parseToSmiles(name)
    except:
        out = None
    return out
